"""
graph.py
--------
LangGraph wiring updated to:
  - Fix "intnet" typo → "intent"
  - Inject LLM config, ProjectFilesController, and CodebaseIndexer
    into every node that needs them via functools.partial
  - Pass config from environment (no hardcoded keys)
"""

from functools import partial

from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from helpers import get_settings
from models.QuickTasks.states import AgentState
from models.QuickTasks.nodes import (
    intent_node,
    code_task_node,
    code_generator_node,
    autocomplete_node,
    bug_detector_node,
    code_explainer_node,
    code_audit_node,
    code_refine_node,
)
from models.QuickTasks.nodes.file_writer_node import file_writer_node
from controllers import ProjectFilesController
from stores.CodeBaseVDB import CodebaseIndexer


# ════════════════════════════════════════════════════════════════════
# Settings & shared dependencies
# ════════════════════════════════════════════════════════════════════

app_settings = get_settings()

llm_config = {
    "api_url": app_settings.OPENAI_API_URL,
    "api_key":  app_settings.OPENAI_API_KEY,
}

project_controller = ProjectFilesController(
    embedding_api_key = app_settings.OPENAI_API_KEY,
    embedding_api_url = app_settings.OPENAI_API_URL,
)

codebase_indexer = CodebaseIndexer(
    openai_api_key = app_settings.OPENAI_API_KEY,
    openai_api_url = app_settings.OPENAI_API_URL,
)


# ════════════════════════════════════════════════════════════════════
# Router
# ════════════════════════════════════════════════════════════════════

def task_router(state: AgentState) -> str:
    intent = state.intent.value if state.intent else ""

    routes = {
        "generate_code": "code_generator",
        "explain_code":  "code_explainer",
        "bug_detection": "bug_detector",
        "autocomplete":  "autocomplete",
        "refactor":      "code_generator",  # refactor → generate with existing code
    }

    return routes.get(intent, "code_generator")  # safe fallback


# ════════════════════════════════════════════════════════════════════
# Graph
# ════════════════════════════════════════════════════════════════════

graph = StateGraph(AgentState)

# ── Nodes ─────────────────────────────────────────────────────────

graph.add_node("intent",      partial(intent_node,     config=llm_config))
graph.add_node("code_task",   partial(code_task_node,  config=llm_config))

graph.add_node("code_generator", partial(
    code_generator_node,
    config             = llm_config,
    project_controller = project_controller,
    codebase_indexer   = codebase_indexer,
))

graph.add_node("autocomplete", partial(
    autocomplete_node,
    config             = llm_config,
    project_controller = project_controller,
    codebase_indexer   = codebase_indexer,
))

graph.add_node("bug_detector", partial(
    bug_detector_node,
    config             = llm_config,
    project_controller = project_controller,
    codebase_indexer   = codebase_indexer,
))

graph.add_node("code_explainer", partial(
    code_explainer_node,
    config             = llm_config,
    project_controller = project_controller,
    codebase_indexer   = codebase_indexer,
))

graph.add_node("code_audit",    partial(code_audit_node,  config=llm_config, detailed=True))
graph.add_node("code_refine",   partial(code_refine_node, config=llm_config, codebase_indexer=codebase_indexer))
graph.add_node("file_writer",   partial(file_writer_node, config=llm_config))


# ── Edges ─────────────────────────────────────────────────────────

graph.add_edge(START, "intent")
graph.add_edge("intent", "code_task")

graph.add_conditional_edges(
    "code_task",
    task_router,
    {
        "code_generator": "code_generator",
        "code_explainer": "code_explainer",
        "bug_detector":   "bug_detector",
        "autocomplete":   "autocomplete",
    }
)

# Explain goes straight to END (no code produced, nothing to write)
graph.add_edge("code_explainer", END)

# All code-producing nodes → audit → refine → file_writer → END
graph.add_edge("code_generator", "code_audit")
graph.add_edge("bug_detector",   "code_audit")
graph.add_edge("autocomplete",   "code_audit")

graph.add_edge("code_audit",  "code_refine")
graph.add_edge("code_refine", "file_writer")
graph.add_edge("file_writer", END)


# ════════════════════════════════════════════════════════════════════
# Compile
# ════════════════════════════════════════════════════════════════════

memory   = MemorySaver()
AppGraph = graph.compile(checkpointer=memory)
