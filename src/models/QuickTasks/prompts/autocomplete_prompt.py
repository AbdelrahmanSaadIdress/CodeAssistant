import json
from models.QuickTasks.states import AutocompleteResult
from .util import _format_rag_sections

def build_autocomplete_messages(state) -> list:
    rag_section = _format_rag_sections(state)

    messages = [
        {
            "role": "system",
            "content": "\n".join([
                "You are an advanced AI code completion engine similar to GitHub Copilot.",
                "",
                "Your task is to complete a partially written code snippet.",
                "",
                "You will be given two types of reference context:",
                "1. Project Context — surrounding code from the user's project.",
                "   Use this to understand imports, helpers, and naming conventions already in use.",
                "2. Codebase Reference — function-level examples from real GitHub repos.",
                "   Use these as idiomatic patterns for completing the snippet correctly.",
                "",
                "Guidelines:",
                "- Continue the code logically from the last line.",
                "- Preserve the programming language, indentation, and formatting.",
                "- Maintain the same coding style and variable naming as the user's project.",
                "- Do NOT rewrite or modify the existing code.",
                "- Only append the missing code.",
                "",
                "Output Requirements:",
                "- Return ONLY valid JSON.",
                "- completion: ONLY the newly generated continuation.",
                "- full_code: the original snippet + the completion.",
            ])
        },
        {
            "role": "user",
            "content": "\n".join([
                "## Partial Code",
                state.code_context.code or "",
                "",
                "## Retrieved Context",
                rag_section,
                "",
                "## Output Schema",
                json.dumps(AutocompleteResult.model_json_schema(), indent=2),
                "",
                "```json"
            ])
        }
    ]
    return messages

