import os
from dotenv import load_dotenv
load_dotenv()

from helpers import get_settings, Settings

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

# ===========================
# Settings
# ===========================
app_settings: Settings = get_settings()
# ===========================
# Graph State
# ===========================
from ..states import AgentState
# ===========================
# Initialize Graph
# ===========================
graph = StateGraph(AgentState)
# ===========================
# Add Your Nodes Here
# ===========================
from ..nodes import *
graph.add_node("intnet", intent_node)
graph.add_node("code_task", code_task_node)
def task_router(state: AgentState) -> str:
    intent = state.intent.value

    if intent == "generate_code":
        return "code_generator"

    elif intent == "explain_code":
        return "code_explainer"

    elif intent == "bug_detection":
        return "bug_detector"

    elif intent == "autocomplete":
        return "autocomplete"

    return "code_generator"  # fallback
graph.add_node("code_generator", code_generator_node)
graph.add_node("code_explainer", code_explainer_node)
graph.add_node("bug_detector", bug_detector_node)
graph.add_node("autocomplete", autocomplete_node)
graph.add_node("code_audit", code_audit_node)
graph.add_node("code_refine", code_refine_node)




# ===========================
# Add Your Edges Here
# ===========================
graph.add_edge(START, "intnet")
graph.add_edge("intnet", "code_task")

graph.add_conditional_edges(
    "code_task",
    task_router,
    {
        "code_generator": "code_generator",
        "code_explainer": "code_explainer",
        "bug_detector": "bug_detector",
        "autocomplete": "autocomplete"
    }
)

graph.add_edge("code_explainer", END)

graph.add_edge("code_generator", "code_audit")
graph.add_edge("bug_detector", "code_audit")
graph.add_edge("autocomplete", "code_audit")

graph.add_edge("code_audit", "code_refine")
graph.add_edge("code_refine", END)


# ===========================
# Memory
# ===========================

memory = MemorySaver()


# ===========================
# Compile Graph
# ===========================

AppGraph = graph.compile(checkpointer=memory)


# ===========================
# Optional: Save Graph Image
# ===========================

# save_graph_png(AppGraph, filename="graph.png")