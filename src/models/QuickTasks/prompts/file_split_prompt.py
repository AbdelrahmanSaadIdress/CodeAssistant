"""
file_split_prompt.py
--------------------
Asks the LLM to decide whether the refined code should live in one file
or be split across multiple files, and if split, to return each file's
name and content separately.
"""

import json
from models.QuickTasks.states import FileSplitResult


def build_file_split_messages(state) -> list:
    code = state.last_code or state.result or ""

    messages = [
        {
            "role": "system",
            "content": "\n".join([
                "You are a senior Python architect.",
                "",
                "Your task is to decide whether the provided code should be saved",
                "as a single file or split across multiple files.",
                "",
                "Rules for splitting:",
                "- Split if the code contains multiple clearly distinct classes or modules.",
                "- Split if the code contains both a data model and business logic.",
                "- Split if any single logical unit exceeds ~100 lines.",
                "- Split if there are clearly separable concerns (e.g. routes, models, utils).",
                "- Do NOT split if the code is a single function, class, or script.",
                "- Do NOT split if the code is under 60 lines total.",
                "- Do NOT split autocomplete results — they are always one file.",
                "",
                "Naming Rules:",
                "- Use snake_case filenames with .py extension.",
                "- Name each file after its primary responsibility.",
                "  e.g. 'user_model.py', 'auth_router.py', 'database.py'",
                "",
                "Output Rules:",
                "- Return ONLY valid JSON matching the schema.",
                "- Each file entry must have: file_name and content.",
                "- The content must be the COMPLETE code for that file.",
                "- Do NOT truncate or summarise — include the full code.",
                "- Do NOT include explanations outside JSON.",
            ])
        },
        {
            "role": "user",
            "content": "\n".join([
                "## Refined Code",
                code,
                "",
                f"## Intent\n{state.intent.value if state.intent else 'unknown'}",
                "",
                "## Output Schema",
                json.dumps(FileSplitResult.model_json_schema(), indent=2),
                "",
                "## Output",
                "```json"
            ])
        }
    ]

    return messages
