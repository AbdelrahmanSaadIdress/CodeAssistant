import json
from models.QuickTasks.states import CodeRefinementResult
from .util import _format_rag_sections

def build_refine_code_messages(state) -> list:
    codebase_docs = state.codebase_context.documents
    codebase_section = (
        "\n---\n".join(codebase_docs)
        if codebase_docs
        else "No codebase reference available."
    )

    messages = [
        {
            "role": "system",
            "content": "\n".join([
                "You are a senior Python developer.",
                "",
                "Your task is to refine the provided Python code.",
                "",
                "You may be given Codebase Reference — real docstring and comment",
                "patterns from popular Python libraries.",
                "Use these as a style guide for the docstrings and comments you add.",
                "",
                "Guidelines:",
                "- Add docstrings to all functions and classes.",
                "- Add inline comments explaining important lines or logic.",
                "- Do NOT change the functionality of the code.",
                "- Preserve variable names, formatting, and indentation.",
                "- Return ONLY valid JSON following the schema.",
                "- Do NOT include explanations outside JSON.",
            ])
        },
        {
            "role": "user",
            "content": "\n".join([
                f"## Code to Refine\n{state.last_code or state.code_context.code or ''}",
                "",
                "## Codebase Reference (docstring/comment style examples)",
                codebase_section,
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
