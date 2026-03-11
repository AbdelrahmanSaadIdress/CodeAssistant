import json
from models.QuickTasks.states import AutocompleteResult


def build_autocomplete_messages(state):

    messages = [
        {
            "role": "system",
            "content": "\n".join([
                "You are an advanced AI code completion engine similar to GitHub Copilot.",
                "",
                "Your task is to complete a partially written code snippet.",
                "",
                "Guidelines:",
                "- Continue the code logically from the last line.",
                "- Preserve the programming language.",
                "- Preserve the indentation and formatting.",
                "- Maintain the same coding style and variable naming.",
                "- Do NOT rewrite or modify the existing code.",
                "- Only append the missing code.",
                "",
                "Output Requirements:",
                "- Return ONLY valid JSON.",
                "- Do NOT include markdown.",
                "- Do NOT include explanations.",
                "- The completion must begin exactly where the snippet ends.",
                "",
                "Definitions:",
                "completion: ONLY the newly generated continuation.",
                "full_code: the original snippet + the completion."
            ])
        },
        {
            "role": "user",
            "content": "\n".join([
                "Complete the following code snippet.",
                "",
                "### Partial Code",
                state.code_context.code or "",
                "",
                "### Output Schema",
                json.dumps(AutocompleteResult.model_json_schema(), indent=2),
                "",
                "### Instructions",
                "1. Continue the code naturally.",
                "2. Do NOT modify existing lines.",
                "3. Only add missing lines.",
                "",
                "### Output",
                "```json"
            ])
        }
    ]

    return messages