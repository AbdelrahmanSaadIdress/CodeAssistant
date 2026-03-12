from ..states import AgentState
from ..prompts import *
from stores.llm.llm_util import call_llm
import json

config = {
    "api_url":"https://models.github.ai/inference",
    "api_key":"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"
}

from models.QuickTasks.states import CodeAuditResult


def code_audit_node(
    state:    AgentState,
    config:   dict,
    detailed: bool = True,
) -> AgentState:
    print("── CODE AUDIT NODE ──")

    messages = (
        build_detailed_audit_messages(state)
        if detailed
        else build_short_audit_messages(state)
    )

    result = call_llm(config, messages)
    parsed = CodeAuditResult(**result)

    state.audit_context = parsed
    state.audit_history.append(parsed)

    if parsed.fixed_code:
        state.result    = parsed.fixed_code
        state.last_code = parsed.fixed_code

    return state
