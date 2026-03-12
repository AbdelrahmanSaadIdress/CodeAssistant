from fastapi import APIRouter, BackgroundTasks, Depends

from stores.CodeBaseVDB import CodebaseIndexer
from helpers import get_settings, Settings

codebase_router = APIRouter(
    prefix="/api/v1/codebase",
    tags=["Codebase"],
)


# ── Dependency ──────────────────────────────────────────────────────

def get_indexer(settings: Settings = Depends(get_settings)) -> CodebaseIndexer:
    return CodebaseIndexer(
        openai_api_key = settings.OPENAI_API_KEY,
        openai_api_url = getattr(settings, "OPENAI_API_URL", None),
    )


# ── Routes ──────────────────────────────────────────────────────────

@codebase_router.post("/index")
async def trigger_indexing(
    background_tasks: BackgroundTasks,
    indexer: CodebaseIndexer = Depends(get_indexer),
):
    """
    Manually trigger a full re-index of all curated GitHub repos.
    Clones or pulls each repo, then chunks, embeds, and upserts
    all Python files into the shared codebase vector DB.
    Runs in the background — returns immediately.
    """
    background_tasks.add_task(indexer.run)

    return {
        "message": "Codebase indexing started in the background.",
        "status":  "indexing",
    }


@codebase_router.get("/status")
async def index_status(
    indexer: CodebaseIndexer = Depends(get_indexer),
):
    """Check how many chunks are currently in the shared codebase DB."""
    count = indexer.collection_count()

    return {
        "collection":   "codebase-reference",
        "total_chunks": count,
        "indexed":      count > 0,
    }
