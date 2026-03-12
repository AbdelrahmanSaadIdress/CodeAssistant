"""
project_files_controller.py (updated)
--------------------------------------
Handles loading project files AND triggering the chunking + embedding pipeline.
"""

import logging
from pathlib import Path
from typing import List, Optional

from fastapi import UploadFile
import os

from stores.vectorDB.code_chunker import FileChunker, CodeChunk
from stores.vectorDB.embedding_service import EmbeddingService

logger = logging.getLogger(__name__)


class ProjectFilesController:
    """
    Responsible for:
    1. Loading raw file records from disk.
    2. Chunking those files into semantic units.
    3. Embedding and storing them in the vector store.
    4. Exposing retrieval for the LLM context pipeline.
    """

    def __init__(
        self,
        base_dir:          str = "assets/projects",
        embedding_api_key: str = "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",
        embedding_api_url: Optional[str] = "https://models.github.ai/inference",
    ):
        self.base_dir  = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

        self._chunker   = FileChunker()
        self.embedding_api_key = embedding_api_key
        self.embedding_api_url = embedding_api_url
        self._embedder = None


    # ------------------------------------------------------------------
    # File loading
    # ------------------------------------------------------------------

    def load_project_files(self, project_id: str) -> List[dict]:
        """Return raw file records (file_name, path, content) for a project."""
        self._embedder  = EmbeddingService(
            api_key = self.embedding_api_key,
            api_url = self.embedding_api_url,
            persist_dir = os.path.join("assets/vector_store", project_id)
        )
        project_folder = self.base_dir / project_id

        if not project_folder.exists():
            logger.warning("Project folder not found: %s", project_folder)
            return []

        records = []
        for file in project_folder.rglob("*"):
            if not file.is_file():
                continue
            try:
                content = file.read_text(encoding="utf-8")
            except Exception:
                content = ""   # binary file — chunker will skip it

            records.append({
                "file_name": file.name,
                "path":      str(file),
                "content":   content,
            })

        return records

    # ------------------------------------------------------------------
    # Chunking + Embedding pipeline
    # ------------------------------------------------------------------

    def index_project(self, project_id: str) -> int:
        """
        Full pipeline: load → chunk → embed → store.
        Call this after a project is uploaded/extracted.

        Returns the total number of chunks indexed.
        """
        logger.info("Indexing project '%s'...", project_id)

        # 1. Load raw files
        file_records = self.load_project_files(project_id)
        if not file_records:
            logger.warning("No files found for project '%s'.", project_id)
            return 0

        # 2. Chunk
        chunks: List[CodeChunk] = self._chunker.chunk_project(file_records)
        logger.info("Created %d chunks from %d files.", len(chunks), len(file_records))

        # 3. Wipe stale vectors so re-uploads stay consistent
        self._embedder.delete_project(project_id)

        # 4. Embed + store
        stored = self._embedder.embed_and_store(project_id, chunks)
        logger.info("Indexed %d chunks for project '%s'.", stored, project_id)
        self.num_chunks = stored

        return stored


    def chunk_count(self, proj):
        return self.num_chunks

    # ------------------------------------------------------------------
    # Retrieval (used by the LLM context pipeline)
    # ------------------------------------------------------------------

    def retrieve_context(
        self,
        project_id: str,
        query:      str,
        top_k:      int = 5,
    ) -> List[str]:
        """
        Retrieve the top-k most relevant code chunks for a query.
        Returns a list of formatted strings ready to be injected
        into an LLM prompt as context.
        """

        self._embedder  = EmbeddingService(
            api_key = self.embedding_api_key,
            api_url = self.embedding_api_url,
            persist_dir = os.path.join("assets/vector_store", project_id)
        )

        results = self._embedder.retrieve(
            project_id = project_id,
            query      = query,
            top_k      = top_k,
        )
        context_blocks = []
        for r in results:
            meta    = r["metadata"]
            content = r["content"]
            score   = r["score"]

            block = (
                f"# [{meta['chunk_type']}] {meta['name']} "
                f"({meta['file_name']} L{meta['start_line']}–{meta['end_line']}) "
                f"[relevance: {score}]\n"
                f"{content}"
            )
            context_blocks.append(block)

        return context_blocks
