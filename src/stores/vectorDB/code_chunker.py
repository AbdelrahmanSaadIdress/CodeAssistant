"""
code_chunker.py
---------------
AST-aware chunking for source code files.

Splits code into meaningful semantic units (functions, classes, imports)
rather than naive character/token windows that break code context.

Supports Python natively via AST. Falls back to recursive character
splitting for non-Python or unparseable files.
"""

import ast
import uuid
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import List, Optional


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

class ChunkType(str, Enum):
    FUNCTION   = "function"
    CLASS      = "class"
    IMPORTS    = "imports"
    MODULE     = "module"       # top-level statements that are not imports
    PLAIN_TEXT = "plain_text"   # non-code files


@dataclass
class CodeChunk:
    """A single semantic unit extracted from a source file."""

    chunk_id:   str       # unique identifier
    file_name:  str       # e.g. "math_ops.py"
    file_path:  str       # full relative path
    chunk_type: ChunkType
    name:       str       # function/class name, or "imports" / "module"
    content:    str       # the actual source text for this chunk
    start_line: int
    end_line:   int
    language:   str       # "python", "text", "config", …

    # Will be populated by the EmbeddingService later
    embedding: Optional[List[float]] = field(default=None, repr=False)

    def metadata(self) -> dict:
        """Return a flat dict suitable for a vector-DB metadata payload."""
        return {
            "chunk_id":   self.chunk_id,
            "file_name":  self.file_name,
            "file_path":  self.file_path,
            "chunk_type": self.chunk_type.value,
            "name":       self.name,
            "start_line": self.start_line,
            "end_line":   self.end_line,
            "language":   self.language,
        }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_SUPPORTED_CODE_EXTENSIONS = {".py", ".js", ".ts", ".java", ".cpp", ".c", ".go"}
_TEXT_EXTENSIONS            = {".md", ".txt", ".rst", ".yaml", ".yml", ".toml", ".cfg", ".ini", ".env"}
_CONFIG_EXTENSIONS          = {".json", ".xml", ".html", ".css"}
_SKIP_EXTENSIONS            = {".rar", ".zip", ".tar", ".gz", ".bin", ".exe", ".pyc"}


def _detect_language(file_name: str) -> str:
    ext = Path(file_name).suffix.lower()
    mapping = {
        ".py": "python", ".js": "javascript", ".ts": "typescript",
        ".java": "java", ".cpp": "cpp", ".c": "c", ".go": "go",
        ".md": "markdown", ".txt": "text", ".rst": "restructuredtext",
        ".yaml": "yaml", ".yml": "yaml", ".toml": "toml",
        ".cfg": "config", ".ini": "config", ".env": "config",
        ".json": "json", ".xml": "xml", ".html": "html", ".css": "css",
    }
    return mapping.get(ext, "unknown")


def _make_id() -> str:
    return str(uuid.uuid4())


# ---------------------------------------------------------------------------
# Python AST Chunker
# ---------------------------------------------------------------------------

class PythonASTChunker:
    """
    Extracts semantic chunks from a Python source file using the AST.

    Strategy
    --------
    1. Parse the file into an AST.
    2. Walk top-level nodes only (we do NOT recurse into nested classes/funcs
        — they belong to their parent chunk).
    3. Bucket: Import statements → one "imports" chunk.
                FunctionDef / AsyncFunctionDef → one chunk each.
                ClassDef → one chunk (includes all methods).
                Everything else → aggregated into a "module" chunk.
    """

    def chunk(self, file_name: str, file_path: str, source: str) -> List[CodeChunk]:
        try:
            tree = ast.parse(source)
        except SyntaxError:
            # Graceful fallback — treat as plain text
            return _plain_text_chunks(file_name, file_path, source, language="python")

        lines = source.splitlines(keepends=True)
        chunks: List[CodeChunk] = []

        import_lines:  List[ast.stmt] = []
        module_stmts:  List[ast.stmt] = []

        for node in ast.iter_child_nodes(tree):          # top-level only
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                import_lines.append(node)

            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                chunk_src = self._extract_source(lines, node)
                chunks.append(CodeChunk(
                    chunk_id   = _make_id(),
                    file_name  = file_name,
                    file_path  = file_path,
                    chunk_type = ChunkType.FUNCTION,
                    name       = node.name,
                    content    = chunk_src,
                    start_line = node.lineno,
                    end_line   = node.end_lineno,
                    language   = "python",
                ))

            elif isinstance(node, ast.ClassDef):
                chunk_src = self._extract_source(lines, node)
                chunks.append(CodeChunk(
                    chunk_id   = _make_id(),
                    file_name  = file_name,
                    file_path  = file_path,
                    chunk_type = ChunkType.CLASS,
                    name       = node.name,
                    content    = chunk_src,
                    start_line = node.lineno,
                    end_line   = node.end_lineno,
                    language   = "python",
                ))

            else:
                module_stmts.append(node)

        # --- imports chunk ---
        if import_lines:
            start = import_lines[0].lineno
            end   = import_lines[-1].end_lineno
            chunks.insert(0, CodeChunk(
                chunk_id   = _make_id(),
                file_name  = file_name,
                file_path  = file_path,
                chunk_type = ChunkType.IMPORTS,
                name       = "imports",
                content    = "".join(lines[start - 1 : end]),
                start_line = start,
                end_line   = end,
                language   = "python",
            ))

        # --- module-level statements chunk ---
        if module_stmts:
            start = module_stmts[0].lineno
            end   = module_stmts[-1].end_lineno
            chunks.append(CodeChunk(
                chunk_id   = _make_id(),
                file_name  = file_name,
                file_path  = file_path,
                chunk_type = ChunkType.MODULE,
                name       = "module_body",
                content    = "".join(lines[start - 1 : end]),
                start_line = start,
                end_line   = end,
                language   = "python",
            ))

        return chunks

    @staticmethod
    def _extract_source(lines: List[str], node: ast.AST) -> str:
        return "".join(lines[node.lineno - 1 : node.end_lineno])


# ---------------------------------------------------------------------------
# Plain-text / fallback chunker (sliding window with overlap)
# ---------------------------------------------------------------------------

def _plain_text_chunks(
    file_name: str,
    file_path: str,
    content:   str,
    language:  str = "text",
    chunk_size: int = 500,      # characters
    overlap:    int = 50,
) -> List[CodeChunk]:
    """
    Recursive character split with overlap.
    Used for non-Python files and as a fallback.
    """
    if not content.strip():
        return []

    chunks: List[CodeChunk] = []
    start = 0
    part  = 0
    total = len(content)

    while start < total:
        end     = min(start + chunk_size, total)
        snippet = content[start:end]

        # Count lines for metadata
        preceding_newlines = content[:start].count("\n")
        start_line = preceding_newlines + 1
        end_line   = start_line + snippet.count("\n")

        chunks.append(CodeChunk(
            chunk_id   = _make_id(),
            file_name  = file_name,
            file_path  = file_path,
            chunk_type = ChunkType.PLAIN_TEXT,
            name       = f"chunk_{part}",
            content    = snippet,
            start_line = start_line,
            end_line   = end_line,
            language   = language,
        ))

        start += chunk_size - overlap
        part  += 1

    return chunks


# ---------------------------------------------------------------------------
# Public API: FileChunker
# ---------------------------------------------------------------------------

class FileChunker:
    """
    Dispatches files to the appropriate chunking strategy.

    Usage
    -----
    chunker = FileChunker()
    chunks  = chunker.chunk_file(file_record)

    Where `file_record` is a dict with keys:
        file_name : str
        path      : str
        content   : str
    """

    def __init__(self, plain_chunk_size: int = 500, plain_overlap: int = 50):
        self._python_chunker   = PythonASTChunker()
        self._plain_chunk_size = plain_chunk_size
        self._plain_overlap    = plain_overlap

    # ------------------------------------------------------------------
    def chunk_file(self, file_record: dict) -> List[CodeChunk]:
        """Chunk a single file record. Returns [] for binary/skipped files."""
        file_name = file_record.get("file_name", "")
        file_path = file_record.get("path", "")
        content   = file_record.get("content", "") or ""

        ext = Path(file_name).suffix.lower()

        # Skip binary / archive files
        if ext in _SKIP_EXTENSIONS or not content.strip():
            return []

        language = _detect_language(file_name)

        if ext == ".py":
            return self._python_chunker.chunk(file_name, file_path, content)

        # All other text-based files
        return _plain_text_chunks(
            file_name  = file_name,
            file_path  = file_path,
            content    = content,
            language   = language,
            chunk_size = self._plain_chunk_size,
            overlap    = self._plain_overlap,
        )

    # ------------------------------------------------------------------
    def chunk_project(self, file_records: List[dict]) -> List[CodeChunk]:
        """Chunk an entire project (list of file records)."""
        all_chunks: List[CodeChunk] = []
        for record in file_records:
            all_chunks.extend(self.chunk_file(record))
        return all_chunks
