import json
from models.QuickTasks.states import CodeContext

def build_code_task_messages(user_prompt: str):
    messages = [
        {
            "role": "system",
            "content": "\n".join([
                "You are an AI system that analyzes coding requests.",
                "",
                "Your job is to extract structured information from the user's request.",
                "",
                "You must determine:",
                "1. What the user is trying to do (their actual task or intent).",
                "2. Whether the user included a code snippet.",
                "",
                "Important Rules:",
                "- DO NOT generate or invent any code.",
                "- Only extract code that the user explicitly provided.",
                "- If the user did NOT include code, the 'code' field must be an empty string.",
                "- If the user's request is vague, infer the most likely task based on context.",
                "- Do NOT explain anything.",
                "- Output ONLY valid JSON that follows the schema."
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
                "## Extraction Instructions",
                "1. Identify the user's main coding task or goal.",
                "2. Extract any code snippet exactly as written by the user.",
                "3. If no code snippet exists, set the 'code' field to an empty string.",
                "4. Do not modify or improve the user's code.",
                "5. Do not generate new code.",
                "",
                "## Output Format",
                "Return ONLY a JSON object matching the schema.",
                "",
                "## Output",
                "```json"
            ])
        }
    ]

    return messages