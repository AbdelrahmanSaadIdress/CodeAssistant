from fastapi import APIRouter, Body, Depends, HTTPException

from models.QuickTasks.states import AgentState
from models.QuickTasks.Graphs.graph import AppGraph
from helpers import get_settings, Settings

quick_tasks_router = APIRouter(
    prefix="/api/v1/quick-tasks",
    tags=["QuickTasks"],
)


# ── Routes ──────────────────────────────────────────────────────────

@quick_tasks_router.post("/help")
async def quick_help(
    project_id:          str  = Body(...,   embed=True),
    prompt:              str  = Body(...,   embed=True),
    use_project_context: bool = Body(False, embed=True),
):
    """
    Main endpoint for the code assistant.

    Request body:
        project_id           –  identifies which project vector DB to query
        prompt               –  the user's coding question or code snippet
        use_project_context  –  if true, retrieves relevant chunks from the
                                user's project DB before calling the LLM.
                                The codebase reference DB is always queried
                                regardless of this flag (happens inside the nodes).

    Flow:
        intent_node → code_task_node → [generate | autocomplete | bug | explain]
                                            → code_audit_node → code_refine_node
    """

    state = AgentState(
        user_input  = prompt,
        project_id  = project_id if use_project_context else None,
    )

    config = {"configurable": {"thread_id": project_id}}

    try:
        result: AgentState = AppGraph.invoke(state, config=config)
    except Exception as exc:
        raise HTTPException(
            status_code = 500,
            detail      = f"Agent execution failed: {str(exc)}",
        )

    return {
        "project_id":   project_id,
        "intent":       result["intent"].value if result["intent"] else None,
        "result":       result["result"],
        "last_code":    result['last_code'],
        "audit":        result['audit_context'].model_dump() if result['audit_context'] else None,
        "output_files": [f.model_dump() for f in result['output_files']],
        "context_used": {
            "project_chunks":  len(result['retrieval_context'].documents),
            "codebase_chunks": len(result['codebase_context'].documents),
        },
    }
