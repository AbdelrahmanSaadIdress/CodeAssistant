from ..states import AgentState
from ..prompts import *
from stores.llm.llm_util import call_llm
from langchain_core.runnables import RunnableConfig




from controllers import ProjectFilesController
from stores.CodeBaseVDB import CodebaseIndexer

from .utils import _populate_rag_context


def bug_detector_node(
    state:              AgentState,
    config:             RunnableConfig,
    project_controller: ProjectFilesController,
    codebase_indexer:   CodebaseIndexer,
) -> AgentState:
    print("── BUG DETECTOR NODE ──")

    # Only pull project context — we want to understand the user's
    # own helpers/imports, not external library internals
    if state.project_id:
        project_chunks = project_controller.retrieve_context(
            project_id = state.project_id,
            query      = state.task or state.user_input,
            top_k      = 4,
        )
        state.retrieval_context.documents = project_chunks

    messages = build_bug_messages(state)
    result   = call_llm(config, messages)

    state.result    = result.get("bugs")
    state.last_code = result.get("fixed_code")

    return state