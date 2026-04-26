from ..states import AgentState
from ..prompts import *
from stores.llm.llm_util import call_llm


from controllers import ProjectFilesController
from stores.CodeBaseVDB import CodebaseIndexer

from .utils import _populate_rag_context


def code_explainer_node(
    state:              AgentState,
    config:             dict,
    project_controller: ProjectFilesController,
    codebase_indexer:   CodebaseIndexer,
) -> AgentState:
    print("── EXPLAIN NODE ──")

    if state.project_id:
        project_chunks = project_controller.retrieve_context(
            project_id = state.project_id,
            query      = state.task or state.user_input,
            top_k      = 4,
        )
        state.retrieval_context.documents = project_chunks

    messages = build_explain_messages(state)
    result   = call_llm(config, messages)

    state.result = result.get("explanation")

    return state

