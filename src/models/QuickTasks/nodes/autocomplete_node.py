from ..states import AgentState
from ..prompts import *
from stores.llm.llm_util import call_llm

config = {
    "api_url":"https://models.github.ai/inference",
    "api_key":"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"
}

def autocomplete_node(state: AgentState) -> AgentState:
    print("AUTOCOMP NODE...")

    messages = build_autocomplete_messages(state)

    result = call_llm(config, messages)
    print(result)


    state.result = result.get("completion")
    state.last_code = result.get("full_code")

    return state