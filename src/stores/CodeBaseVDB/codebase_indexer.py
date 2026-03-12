
import logging
import os
import subprocess
from pathlib import Path
from typing import List, Optional

import chromadb
from chromadb.config import Settings as ChromaSettings
from openai import OpenAI

from ..vectorDB.code_chunker import PythonASTChunker, CodeChunk, _plain_text_chunks
from .codebase_config import (
    CURATED_REPOS,
    RepoConfig,
    MAX_FILES_PER_REPO,
    MAX_FILE_SIZE_BYTES,
    REPOS_CLONE_DIR,
    CODEBASE_COLLECTION,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

EMBEDDING_MODEL    = "openai/text-embedding-3-small"   # 1536 dims, very cost-effective
BATCH_SIZE      = 50



class CodebaseIndexer:
    """
    Manages the shared codebase vector DB.

    Workflow per repo
    -----------------
    1. clone_or_update()  → repo on disk
    2. collect_py_files() → list of .py paths
    3. chunk_file()       → CodeChunk list (reuses PythonASTChunker)
    4. embed_and_upsert() → vectors in ChromaDB "codebase-reference" collection
    """

    def __init__(
        self,
        openai_api_key: str,
        openai_api_url: Optional[str] = None,
        chroma_dir:     str = "stores/CodeBaseVDB/storage/chroma",
    ):
        self._openai = OpenAI(
            api_key  = openai_api_key,
            base_url = openai_api_url or None,
        )
        self._chroma = chromadb.PersistentClient(
            path     = chroma_dir,
            settings = ChromaSettings(anonymized_telemetry=False),
        )
        self._chunker   = PythonASTChunker()
        self._clone_dir = Path(REPOS_CLONE_DIR)
        self._clone_dir.mkdir(parents=True, exist_ok=True)

        # Get or create the single shared collection for all repos
        self._collection = self._chroma.get_or_create_collection(
            name     = CODEBASE_COLLECTION,
            metadata = {"hnsw:space": "cosine"},
        )

        logger.info("CodebaseIndexer ready — collection: '%s'", CODEBASE_COLLECTION)

    # ------------------------------------------------------------------
    # Public: index all repos
    # ------------------------------------------------------------------

    def run(self, repos: List[RepoConfig] = CURATED_REPOS) -> dict:
        """
        Full pipeline for all curated repos.
        Returns a summary dict  { repo_name: chunks_indexed }.
        """
        summary = {}
        for repo in repos:
            try:
                logger.info("━━━ Indexing repo: %s ━━━", repo.name)
                count = self._index_repo(repo)
                summary[repo.name] = count
                logger.info("✓ %s → %d chunks", repo.name, count)
            except Exception as exc:
                logger.error("✗ %s failed: %s", repo.name, exc)
                summary[repo.name] = -1

        logger.info("Indexing complete: %s", summary)
        return summary

    # ------------------------------------------------------------------
    # Private: single repo pipeline
    # ------------------------------------------------------------------

    def _index_repo(self, repo: RepoConfig) -> int:
        # 1. Clone or update
        repo_path = self._clone_or_update(repo)
        print(repo_path)
        # 2. Collect .py files respecting include_paths + size limit
        py_files = self._collect_py_files(repo_path, repo.include_paths)
        logger.info("  Found %d .py files (capped at %d)", len(py_files), MAX_FILES_PER_REPO)
        print("=================="*10)
        # 3. Chunk + embed in one streaming pass
        total = 0
        batch_texts:  List[str]       = []
        batch_chunks: List[CodeChunk] = []

        for py_file in py_files:
            file_chunks = self._chunk_file(py_file, repo)
            for chunk in file_chunks:
                batch_texts.append(self._build_embed_text(chunk, repo))
                batch_chunks.append(chunk)

                if len(batch_chunks) >= BATCH_SIZE:
                    total += self._flush(batch_chunks, batch_texts)
                    batch_chunks, batch_texts = [], []

        # flush remainder
        if batch_chunks:
            total += self._flush(batch_chunks, batch_texts)

        return total

    # ------------------------------------------------------------------
    # Git helpers
    # ------------------------------------------------------------------

    def _clone_or_update(self, repo: RepoConfig) -> Path:
        dest = self._clone_dir / repo.name

        if dest.exists():
            logger.info("  Pulling latest: %s", repo.name)
            subprocess.run(
                ["git", "-C", str(dest), "pull", "--ff-only"],
                check=True, capture_output=True,
            )
        else:
            logger.info("  Cloning: %s", repo.url)
            subprocess.run(
                ["git", "clone", "--depth=1", repo.url, str(dest)],
                check=True, capture_output=True,
            )

        return dest

    # ------------------------------------------------------------------
    # File collection
    # ------------------------------------------------------------------

    def _collect_py_files(
        self,
        repo_path:     Path,
        include_paths: List[str],
    ) -> List[Path]:
        """
        Walk the repo and return .py files.
        If include_paths is set, only files inside those sub-folders are included.
        Results are capped at MAX_FILES_PER_REPO.
        """
        candidates: List[Path] = []

        search_roots = (
            [repo_path / p for p in include_paths]
            if include_paths
            else [repo_path]
        )

        for root in search_roots:
            if not root.exists():
                logger.warning("  include_path not found: %s", root)
                continue
            for py_file in sorted(root.rglob("*.py")):
                if self._should_skip(py_file):
                    continue
                candidates.append(py_file)
                if len(candidates) >= MAX_FILES_PER_REPO:
                    return candidates

        return candidates

    @staticmethod
    def _should_skip(path: Path) -> bool:
        """Filter out generated, test, migration, and oversized files."""
        skip_dirs  = {"__pycache__", ".git", "migrations", "node_modules"}
        skip_names = {"setup.py", "conf.py"}   # sphinx conf, etc.

        if any(part in skip_dirs for part in path.parts):
            return True
        if path.name in skip_names:
            return True
        if path.stat().st_size > MAX_FILE_SIZE_BYTES:
            return True
        return False

    # ------------------------------------------------------------------
    # Chunking
    # ------------------------------------------------------------------

    def _chunk_file(self, py_file: Path, repo: RepoConfig) -> List[CodeChunk]:
        try:
            source = py_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return []

        if not source.strip():
            return []

        # Relative path for cleaner metadata (e.g. "fastapi/routing.py")
        try:
            rel_path = str(py_file.relative_to(self._clone_dir))
        except ValueError:
            rel_path = str(py_file)

        chunks = self._chunker.chunk(
            file_name = py_file.name,
            file_path = rel_path,
            source    = source,
        )

        # Tag every chunk with the repo it came from
        for chunk in chunks:
            chunk.language = f"python:{repo.name}"

        return chunks

    # ------------------------------------------------------------------
    # Embedding + upsert
    # ------------------------------------------------------------------

    @staticmethod
    def _build_embed_text(chunk: CodeChunk, repo: RepoConfig) -> str:
        """
        Rich prefix so the embedding captures origin + semantics.

        [repo:fastapi | function | routing.py]
        def include_router(...):
        """
        return (
            f"[repo:{repo.name} | {chunk.chunk_type.value} | {chunk.file_name}]\n"
            f"{chunk.content}"
        )

    def _flush(
        self,
        chunks: List[CodeChunk],
        texts:  List[str],
    ) -> int:
        embeddings = self._embed_batch(texts)
        if embeddings is None:
            return 0

        self._collection.upsert(
            ids        = [c.chunk_id  for c in chunks],
            embeddings = embeddings,
            documents  = [c.content   for c in chunks],
            metadatas  = [
                {**c.metadata(), "repo": c.language.split(":")[-1]}
                for c in chunks
            ],
        )
        return len(chunks)

    def _embed_batch(self, texts: List[str]) -> Optional[List[List[float]]]:
        try:
            response = self._openai.embeddings.create(
                model = EMBEDDING_MODEL,
                input = texts,
            )
            return [item.embedding for item in response.data]
        except Exception as exc:
            logger.error("Embedding error: %s", exc)
            return None

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def collection_count(self) -> int:
        """Return the total number of chunks currently in the codebase DB."""
        try:
            return self._collection.count()
        except Exception:
            return 0

    # ------------------------------------------------------------------
    # Retrieval (used by generate_node / autocomplete_node)
    # ------------------------------------------------------------------

    def retrieve(
        self,
        query:      str,
        top_k:      int = 5,
        repo_filter: Optional[str] = None,   # e.g. "fastapi" to narrow results
    ) -> List[dict]:
        """
        Retrieve the most relevant codebase chunks for a query.
        Returns [{ content, metadata, score }, ...]
        """
        try:
            embedding = self._embed_batch([query])
            if not embedding:
                return []
            where = {"repo": {"$eq": repo_filter}} if repo_filter else None

            results = self._collection.query(
                query_embeddings = embedding,
                n_results        = top_k,
                where            = where,
                include          = ["documents", "metadatas", "distances"],
            )

            docs      = results["documents"][0]
            metas     = results["metadatas"][0]
            distances = results["distances"][0]

            return [
                {
                    "content":  doc,
                    "metadata": meta,
                    "score":    round(1 - dist, 4),
                }
                for doc, meta, dist in zip(docs, metas, distances)
            ]

        except Exception as exc:
            logger.error("Codebase retrieval error: %s", exc)
            return []
