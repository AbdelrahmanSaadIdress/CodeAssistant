import json
from models.QuickTasks.states import CodeContext
from .util import _format_rag_sections

def build_code_task_messages(user_prompt: str) -> list:
    # Extraction node — no RAG context needed.
    messages = [
        {
            "role": "system",
            "content": "\n".join([
                "You are an AI system that analyzes coding requests.",
                "",
                "Your job is to extract structured information from the user's request.",
                "",
                "You must determine:",
                "1. What the user is trying to do (their actual task).",
                "2. Whether the user included a code snippet.",
                "",
                "Important Rules:",
                "- DO NOT generate or invent any code.",
                "- Only extract code that the user explicitly provided.",
                "- If the user did NOT include code, the 'code' field must be null.",
                "- Do NOT explain anything.",
                "- Output ONLY valid JSON that follows the schema.",
            ])
        },
        {
            "role": "user",
            "content": "\n".join([
                f"User Request:\n{user_prompt}",
                "",
                "## Output Schema",
                json.dumps(CodeContext.model_json_schema(), indent=2),
                "",
                "## Output",
                "```json"
            ])
        }
    ]
    return messages

