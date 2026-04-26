from models.QuickTasks.states import AgentState, CodeContext
from models.QuickTasks.prompts import build_code_task_messages
from stores.llm.llm_util import call_llm
from langchain_core.runnables import RunnableConfig



import json 



def code_task_node(state: AgentState, llm_config) -> AgentState:
    print("── CODE TASK NODE ──")

    messages = build_code_task_messages(state.user_input)
    result   = call_llm(llm_config, messages)

    state.code_context.code = result.get("code") or state.code_context.code
    state.task              = result.get("task") or state.task

    return state
