import json
from models.QuickTasks.states import CodeRefinementResult

def build_refine_code_messages(state):

    messages = [
        {
            "role": "system",
            "content": "\n".join([
                "You are a senior Python developer.",
                "",
                "Your task is to refine the provided Python code.",
                "Guidelines:",
                "- Add docstrings to all functions and classes.",
                "- Add inline comments explaining important lines or logic.",
                "- Do NOT change the functionality of the code.",
                "- Preserve variable names, formatting, and indentation.",
                "- Suggest improvements only through comments or docstrings.",
                "- Return ONLY valid JSON following the schema below.",
                "- Do NOT include explanations outside JSON."
            ])
        },
        {
            "role": "user",
            "content": "\n".join([
                f"Code to refine:\n{state.last_code or state.code_context.code or ''}",
                "",
                "## Output Schema",
                json.dumps(CodeRefinementResult.model_json_schema(), indent=2),
                "",
                "## Output",
                "```json"
            ])
        }
    ]

    return messages