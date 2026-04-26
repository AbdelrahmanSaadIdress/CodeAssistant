from ..states import AgentState
from ..prompts import *
from stores.llm.llm_util import call_llm

from controllers import ProjectFilesController
from stores.CodeBaseVDB import CodebaseIndexer

from .utils import _populate_rag_context



def code_generator_node(
    state:              AgentState,
    config:             dict,
    project_controller: ProjectFilesController,
    codebase_indexer:   CodebaseIndexer ) -> AgentState:
    print("── GENERATE NODE ──")

    state = _populate_rag_context(state, project_controller, codebase_indexer)

    messages = build_generate_messages(state)
    result   = call_llm(config, messages)

    state.result    = result.get("code")
    state.last_code = result.get("code")

    return state