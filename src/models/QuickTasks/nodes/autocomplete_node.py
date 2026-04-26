from ..states import AgentState
from ..prompts import *
from stores.llm.llm_util import call_llm


from controllers import ProjectFilesController
from stores.CodeBaseVDB import CodebaseIndexer

from .utils import _populate_rag_context
from langchain_core.runnables import RunnableConfig




def autocomplete_node(
    state:              AgentState,
    config:             RunnableConfig,
    project_controller: ProjectFilesController,
    codebase_indexer:   CodebaseIndexer,
) -> AgentState:
    print("── AUTOCOMPLETE NODE ──")

    # For autocomplete, filter codebase to function chunks only
    query = state.task or state.user_input

    if state.project_id:
        project_chunks = project_controller.retrieve_context(
            project_id = state.project_id,
            query      = query,
            top_k      = 3,
        )
        state.retrieval_context.documents = project_chunks

    codebase_results = codebase_indexer.retrieve(query=query, top_k=3)
    state.codebase_context.documents = [
        r["content"] for r in codebase_results
        if r["metadata"].get("chunk_type") == "function"
    ]

    messages = build_autocomplete_messages(state)
    result   = call_llm(config, messages)

    state.result    = result.get("completion")
    state.last_code = result.get("full_code")

    return state
