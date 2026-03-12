"""
embedding_service.py
--------------------
Embeds CodeChunks and persists them in a ChromaDB vector store.

Design decisions
----------------
- One ChromaDB *collection per project_id* → clean isolation.
- Embeddings use OpenAI text-embedding-3-small (fast, cheap, 1536-dim).
- Upsert semantics: re-uploading a project overwrites stale chunks.
- Retrieval returns the top-k most relevant chunks with their metadata.

Usage
-----
    service = EmbeddingService(api_key="sk-...")
    service.embed_and_store(project_id="saad", chunks=chunks)

    results = service.retrieve(project_id="saad", query="how does add() work?", top_k=5)
"""

import logging
from typing import List, Optional

import chromadb
from chromadb.config import Settings as ChromaSettings
from openai import OpenAI

from .code_chunker import CodeChunk

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

EMBEDDING_MODEL    = "openai/text-embedding-3-small"   # 1536 dims, very cost-effective
EMBEDDING_DIMS     = 1536
CHROMA_PERSIST_DIR = "assets/vector_store"       # persisted on disk


# ---------------------------------------------------------------------------
# EmbeddingService
# ---------------------------------------------------------------------------

class EmbeddingService:
    """
    Manages embedding generation and vector storage for project files.

    Parameters
    ----------
    api_key : str
        OpenAI API key.
    api_url : str, optional
        Custom base URL (e.g. GitHub Models inference endpoint).
    persist_dir : str
        Directory where ChromaDB will persist its data.
    """

    def __init__(
        self,
        api_key:     str = None,
        api_url:     Optional[str] = None,
        persist_dir: str = CHROMA_PERSIST_DIR,
    ):
        self._openai = OpenAI(
            api_key  = api_key,
            base_url = api_url if api_url else None,
        )

        # Persistent ChromaDB client — survives server restarts
        self._chroma = chromadb.PersistentClient(
            path     = persist_dir,
            settings = ChromaSettings(anonymized_telemetry=False),
        )

        logger.info("EmbeddingService initialised (persist_dir=%s)", persist_dir)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def embed_and_store(
        self,
        project_id: str,
        chunks:     List[CodeChunk],
    ) -> int:
        """
        Embed all chunks and upsert them into the project's collection.

        Returns the number of chunks stored.
        """
        if not chunks:
            logger.warning("No chunks to embed for project '%s'.", project_id)
            return 0

        collection = self._get_or_create_collection(project_id)

        # Embed in batches to stay inside API rate limits
        batch_size = 50
        total      = 0

        for i in range(0, len(chunks), batch_size):
            batch = chunks[i : i + batch_size]

            texts      = [self._build_embed_text(c) for c in batch]
            embeddings = self._embed_batch(texts)

            if embeddings is None:
                logger.error("Embedding failed for batch %d — skipping.", i)
                continue

            collection.upsert(
                ids        = [c.chunk_id  for c in batch],
                embeddings = embeddings,
                documents  = [c.content   for c in batch],
                metadatas  = [c.metadata() for c in batch],
            )

            total += len(batch)
            logger.info("Stored %d/%d chunks for project '%s'.", total, len(chunks), project_id)

        return total

    def retrieve(
        self,
        project_id: str,
        query:      str,
        top_k:      int = 5,
        file_name:  Optional[str] = None,   # optional filter by file
        chunk_type: Optional[str] = None,   # optional filter by chunk type
    ) -> List[dict]:
        """
        Retrieve the most relevant chunks for a query.

        Returns a list of dicts, each containing:
            content, metadata, distance
        """
        collection = self._get_collection(project_id)

        if collection is None:
            logger.warning("No vector store found for project '%s'.", project_id)
            return []

        query_embedding = self._embed_single(query)
        if query_embedding is None:
            return []

        # Build optional where-filter for metadata
        where = self._build_where_filter(file_name, chunk_type)

        results = collection.query(
            query_embeddings = [query_embedding],
            n_results        = top_k,
            where            = where if where else None,
            include          = ["documents", "metadatas", "distances"],
        )

        return self._format_results(results)

    def delete_project(self, project_id: str) -> None:
        """Remove all vectors for a project (e.g. on re-upload)."""
        collection_name = self._collection_name(project_id)
        try:
            self._chroma.delete_collection(collection_name)
            logger.info("Deleted collection '%s'.", collection_name)
        except Exception as exc:
            logger.warning("Could not delete collection '%s': %s", collection_name, exc)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _collection_name(project_id: str) -> str:
        # ChromaDB collection names must be alphanumeric + hyphens
        return f"project-{project_id}".replace("_", "-").lower()

    def _get_or_create_collection(self, project_id: str):
        return self._chroma.get_or_create_collection(
            name     = self._collection_name(project_id),
            metadata = {"hnsw:space": "cosine"},   # cosine similarity
        )

    def _get_collection(self, project_id: str):
        try:
            return self._chroma.get_collection(self._collection_name(project_id))
        except Exception:
            return None

    @staticmethod
    def _build_embed_text(chunk: CodeChunk) -> str:
        """
        Prepend rich context before the raw content so the embedding
        captures *what* the chunk is, not just its tokens.

        Example prefix:
            [python | function | math_ops.py]
            def add(a, b): ...
        """
        return (
            f"[{chunk.language} | {chunk.chunk_type.value} | {chunk.file_name}]\n"
            f"{chunk.content}"
        )

    def _embed_batch(self, texts: List[str]) -> Optional[List[List[float]]]:
        try:
            response = self._openai.embeddings.create(
                model = EMBEDDING_MODEL,
                input = texts,
            )
            return [item.embedding for item in response.data]
        except Exception as exc:
            logger.error("OpenAI embedding error: %s", exc)
            return None

    def _embed_single(self, text: str) -> Optional[List[float]]:
        result = self._embed_batch([text])
        return result[0] if result else None

    @staticmethod
    def _build_where_filter(
        file_name:  Optional[str],
        chunk_type: Optional[str],
    ) -> dict:
        conditions = []
        if file_name:
            conditions.append({"file_name": {"$eq": file_name}})
        if chunk_type:
            conditions.append({"chunk_type": {"$eq": chunk_type}})

        if len(conditions) == 1:
            return conditions[0]
        if len(conditions) > 1:
            return {"$and": conditions}
        return {}

    @staticmethod
    def _format_results(raw: dict) -> List[dict]:
        """Flatten ChromaDB's nested response into a clean list."""
        docs      = raw.get("documents", [[]])[0]
        metas     = raw.get("metadatas", [[]])[0]
        distances = raw.get("distances",  [[]])[0]

        return [
            {
                "content":  doc,
                "metadata": meta,
                "score":    round(1 - dist, 4),   # cosine similarity (1 = perfect)
            }
            for doc, meta, dist in zip(docs, metas, distances)
        ]
