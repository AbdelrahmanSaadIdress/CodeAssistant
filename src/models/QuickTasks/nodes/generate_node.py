from ..states import AgentState
from ..prompts import *
from stores.llm.llm_util import call_llm

config = {
    "api_url":"https://models.github.ai/inference",
    "api_key":"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"
}
def code_generator_node(state: AgentState) -> AgentState:
    print("GENERATE NODE...")
    messages = build_generate_messages(state)

    result = call_llm(config, messages)

    state.result = result.get("code")
    state.last_code = result.get("code")

    return state