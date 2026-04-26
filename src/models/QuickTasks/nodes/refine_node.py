from ..states import AgentState, CodeRefinementResult
from ..prompts import *
from stores.llm.llm_util import call_llm
import json


from stores.CodeBaseVDB import CodebaseIndexer

def code_refine_node(
    state:            AgentState,
    config:           dict,
    codebase_indexer: CodebaseIndexer,
) -> AgentState:
    print("── REFINE NODE ──")

    # Pull codebase patterns to guide docstring/comment style
    codebase_results = codebase_indexer.retrieve(
        query  = state.task or state.user_input,
        top_k  = 3,
    )
    state.codebase_context.documents = [r["content"] for r in codebase_results]

    messages = build_refine_code_messages(state)
    result   = call_llm(config, messages)

    parsed = CodeRefinementResult(**result)

    state.last_code = parsed.refined_code
    state.result    = parsed.refined_code

    if parsed.changes:
        state.retrieval_context.documents.append(
            json.dumps({"refinement_changes": parsed.changes})
        )

    return state
