from models.QuickTasks.states import BugDetectionResult
import json


def build_bug_messages(state):

    messages = [
        {
            "role": "system",
            "content": "\n".join([
                "You are a senior debugging expert.",
                "",
                "Your task is to analyze code and detect bugs.",
                "",
                "Rules:",
                "- Identify logical errors",
                "- Identify syntax problems",
                "- Suggest fixes",
                "- Return JSON only"
            ])
        },
        {
            "role": "user",
            "content": "\n".join([
                f"Code:\n{state.code_context.code}",
                "",
                "## Output Schema",
                json.dumps(BugDetectionResult.model_json_schema(), indent=2),
                "",
                "Return JSON only.",
                "",
                "```json"
            ])
        }
    ]

    return messages