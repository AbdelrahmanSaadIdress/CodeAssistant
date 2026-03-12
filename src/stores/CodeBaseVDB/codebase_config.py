"""
codebase_config.py
------------------
Curated list of GitHub repositories to index into the shared codebase DB.

To add a new repo:
    1. Add an entry to CURATED_REPOS.
    2. The weekly cron will pick it up automatically on next run.
    3. To index immediately, run:  python codebase_indexer.py --now
"""

from dataclasses import dataclass, field
from typing import List

@dataclass
class RepoConfig:
    name:           str          # human-readable label
    url:            str          # GitHub clone URL (HTTPS)
    description:    str          # what this repo teaches the LLM
    include_paths:  List[str] = field(default_factory=list)
    # ^ sub-folders to index; empty list = entire repo
    # e.g. ["fastapi/", "tests/"] to skip docs/benchmarks



CURATED_REPOS: List[RepoConfig] = [

    # --- Web Frameworks ---
    RepoConfig(
        name        = "fastapi",
        url         = "https://github.com/tiangolo/fastapi.git",
        description = "FastAPI web framework — routing, dependencies, middleware",
        include_paths = ["fastapi/"],
    ),

    # --- LLM / AI Orchestration ---
    RepoConfig(
        name        = "langchain",
        url         = "https://github.com/langchain-ai/langchain.git",
        description = "LangChain — chains, agents, memory, tools",
        include_paths = ["libs/langchain/langchain/"],
    ),
    RepoConfig(
        name        = "langgraph",
        url         = "https://github.com/langchain-ai/langgraph.git",
        description = "LangGraph — stateful multi-agent graph execution",
        include_paths = ["langgraph/"],
    ),

    # --- Vector Stores / Embeddings ---
    RepoConfig(
        name        = "chromadb",
        url         = "https://github.com/chroma-core/chroma.git",
        description = "ChromaDB — vector store client and server",
        include_paths = ["chromadb/"],
    ),

    # # --- HTTP / Async ---
    # RepoConfig(
    #     name        = "httpx",
    #     url         = "https://github.com/encode/httpx.git",
    #     description = "HTTPX — async HTTP client patterns",
    #     include_paths = ["httpx/"],
    # ),

    # # --- Data Validation ---
    # RepoConfig(
    #     name        = "pydantic",
    #     url         = "https://github.com/pydantic/pydantic.git",
    #     description = "Pydantic v2 — data validation and settings management",
    #     include_paths = ["pydantic/"],
    # ),

    # # --- Database / ORM ---
    # RepoConfig(
    #     name        = "sqlalchemy",
    #     url         = "https://github.com/sqlalchemy/sqlalchemy.git",
    #     description = "SQLAlchemy — ORM, core, async sessions",
    #     include_paths = ["lib/sqlalchemy/"],
    # ),
]

# ---------------------------------------------------------------------------
# Indexing limits (tune these to control DB size vs quality)
# ---------------------------------------------------------------------------


# Max .py files to index per repo (prevents huge repos from taking hours)
MAX_FILES_PER_REPO = 5

# Skip files larger than this (generated code, minified, etc.)
MAX_FILE_SIZE_BYTES = 50_000   # 50 KB

# # Cron schedule (APScheduler cron syntax)
# CRON_DAY_OF_WEEK = "sun"
# CRON_HOUR        = 2
# CRON_MINUTE      = 0
# # → runs every Sunday at 02:00

# Where repos are cloned on disk
REPOS_CLONE_DIR = "stores/CodeBaseVDB/storage/repos"

# ChromaDB collection name for the shared codebase
CODEBASE_COLLECTION = "codebase-reference"

