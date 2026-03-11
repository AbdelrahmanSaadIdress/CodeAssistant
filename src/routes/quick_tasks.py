from fastapi import FastAPI, APIRouter, Depends
from helpers import get_settings, Settings
from .Input_schemas.Input_ import HelpRequest
from models.QuickTasks.states import *



quick_tasks_router = APIRouter(
    prefix="/api/v1",
    tags=["QuickTasks"],
)

from models.QuickTasks.Graphs.graph import AppGraph

@quick_tasks_router.post("/quickHelp")
async def start_helping(
    request: HelpRequest,
    app_settings: Settings = Depends(get_settings)
):
    user_prompt = request.prompt
    print(user_prompt)
    state = AgentState(user_input=user_prompt)
    config = {"configurable": {"thread_id": "user_1"}}
    result = AppGraph.invoke(state, config=config)

    return result