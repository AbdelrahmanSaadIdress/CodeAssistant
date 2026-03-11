from ..states import AgentState, CodeRefinementResult
from ..prompts import *
from stores.llm.llm_util import call_llm
import json

config = {
    "api_url":"https://models.github.ai/inference",
    "api_key":"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"
}

def code_refine_node(state: AgentState) -> AgentState:

    print("REFINING CODE ...")

    messages = build_refine_code_messages(state)
    # Call LLM
    result = call_llm(config, messages)

    # Parse structured output
    parsed = CodeRefinementResult(**result)

    # Update last_code with refined version
    state.last_code = parsed.refined_code
    state.result = parsed.refined_code

    # Optionally store changes in retrieval_context
    if parsed.changes:
        state.retrieval_context.documents.append(json.dumps({
            "refinement_changes": parsed.changes
        }))

    return state