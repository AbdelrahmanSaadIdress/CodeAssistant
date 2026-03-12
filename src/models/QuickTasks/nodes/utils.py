
import json
from models.QuickTasks.states import (
    AgentState,
    Intent,
    CodeContext,
    CodeAuditResult,
    CodeRefinementResult,
)

from stores.llm.llm_util import call_llm
from controllers import ProjectFilesController
from stores.CodeBaseVDB import CodebaseIndexer

def _populate_rag_context(
    state:              AgentState,
    project_controller: ProjectFilesController,
    codebase_indexer:   CodebaseIndexer,
    project_top_k:      int = 4,
    codebase_top_k:     int = 4,
    ) -> AgentState:
    """
    Retrieves from both vector DBs and populates state in-place.
    Uses state.task if available (more specific query), else state.user_input.
    """
    query = state.task or state.user_input

    # ── Project DB ─────────────────────────────────────────────────
    if state.project_id:
        project_chunks = project_controller.retrieve_context(
            project_id = state.project_id,
            query      = query,
            top_k      = project_top_k,
        )
        state.retrieval_context.documents = project_chunks

    # ── Codebase DB ────────────────────────────────────────────────
    codebase_results = codebase_indexer.retrieve(
        query  = query,
        top_k  = codebase_top_k,
    )
    state.codebase_context.documents = [r["content"] for r in codebase_results]

    return state
