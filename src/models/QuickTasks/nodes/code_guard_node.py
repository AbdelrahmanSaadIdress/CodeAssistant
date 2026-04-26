from ..states import AgentState
from ..prompts import *
from stores.llm.llm_util import call_llm
import json



from models.QuickTasks.states import CodeAuditResult
from langchain_core.runnables import RunnableConfig


def code_audit_node(
    state:    AgentState,
    llm_config,
    detailed: bool = True,
) -> AgentState:
    print("── CODE AUDIT NODE ──")

    messages = (
        build_detailed_audit_messages(state)
        if detailed
        else build_short_audit_messages(state)
    )

    result = call_llm(llm_config, messages)
    parsed = CodeAuditResult(**result)

    state.audit_context = parsed
    state.audit_history.append(parsed)

    return state
