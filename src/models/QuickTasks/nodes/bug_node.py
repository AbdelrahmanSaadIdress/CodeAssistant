from ..states import AgentState
from ..prompts import *
from stores.llm.llm_util import call_llm

config = {
    "api_url":"https://models.github.ai/inference",
    "api_key":"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"
}

def bug_detector_node(state: AgentState) -> AgentState:
    print("BUG NODE...")

    messages = build_bug_messages(state)

    result = call_llm(config, messages)
    print(result)

    state.result = result.get("bugs")
    state.last_code = result.get("fixed_code")

    return state