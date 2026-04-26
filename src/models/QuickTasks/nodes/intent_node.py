from models.QuickTasks.states import AgentState, Intent
from models.QuickTasks.prompts import build_intent_messages
from stores.llm.llm_util import call_llm


def intent_node(state: AgentState, config: dict) -> AgentState:
    print("── INTENT NODE ──")

    messages = build_intent_messages(state.user_input)
    result   = call_llm(config, messages)

    if "type" in result:
        state.intent = result["type"]

    return state