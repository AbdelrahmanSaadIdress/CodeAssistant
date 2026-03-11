from models.QuickTasks.states import CodeExplanationResult
import json


def build_explain_messages(state):

    messages = [
        {
            "role": "system",
            "content": "\n".join([
                "You are an expert programming instructor.",
                "",
                "Explain the code clearly and accurately.",
                "",
                "Rules:",
                "- Explain step by step",
                "- Mention important concepts",
                "- Be concise",
                "- Output only JSON"
            ])
        },
        {
            "role": "user",
            "content": "\n".join([
                f"Code:\n{state.code_context.code}",
                "",
                "## Output Schema",
                json.dumps(CodeExplanationResult.model_json_schema(), indent=2),
                "",
                "Return JSON only.",
                "",
                "```json"
            ])
        }
    ]

    return messages