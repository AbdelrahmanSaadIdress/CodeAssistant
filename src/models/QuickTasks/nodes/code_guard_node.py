from ..states import AgentState
from ..prompts import *
from stores.llm.llm_util import call_llm
import json

config = {
    "api_url":"https://models.github.ai/inference",
    "api_key":"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"
}


def code_audit_node(state: AgentState, detailed: bool = True) -> AgentState:

    print("CODE AUDIT ...")

    if detailed:
        messages = build_detailed_audit_messages(state)
    else:
        messages = build_short_audit_messages(state)

    # Call LLM
    result = call_llm(config, messages)

    from models.QuickTasks.states import CodeAuditResult

    # Safely parse result
    parsed = CodeAuditResult(**result)

    # Update state
    state.audit_context = parsed
    state.audit_history.append(parsed)

    # Update main code fields if a fixed version is returned
    if parsed.fixed_code:
        state.result = parsed.fixed_code
        state.last_code = parsed.fixed_code

    return state