from models.QuickTasks.states import AgentState, CodeContext
from models.QuickTasks.prompts import build_code_task_messages
from stores.llm.llm_util import call_llm


import json 

config = {
    "api_url":"https://models.github.ai/inference",
    "api_key":"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"
}


def code_task_node(state: AgentState) -> AgentState:
    # Build messages
    messages = build_code_task_messages(state.user_input)
    
    # Call LLM
    result = call_llm(config, messages)
    # Update state
    state.code_context.code = result.get("code") or state.code_context.code
    state.task = result.get("task") or state.task
    

    print(state)
    return state