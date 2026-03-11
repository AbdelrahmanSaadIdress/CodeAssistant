import json
from models.QuickTasks.states import CodeGenerationResult

def build_generate_messages(state):

    retrieved_docs = "\n\n".join(state.retrieval_context.documents)

    messages = [
        {
            "role": "system",
            "content": "\n".join([
                "You are a senior software engineer.",
                "",
                "Your task is to generate high quality python code.",
                "",
                "Rules:",
                "- Follow best practices",
                "- Write clean and readable code",
                "- Add comments when useful",
                "- Do NOT explain outside JSON",
                "",
                "Return ONLY valid JSON.",
                "The json must follow the **Output Schema** that I will provide you"
            ])
        },
        {
            "role": "user",
            "content": "\n".join([
                f"User Task:\n{state.task}",
                "",
                f"Existing Code:\n{state.code_context.code}",
                "",
                f"Retrieved Context:\n{retrieved_docs}",
                "",
                "## Output Schema",
                json.dumps(CodeGenerationResult.model_json_schema(), indent=2),
                "",
                "Return JSON only.",
                "",
                "```json"
            ])
        }
    ]

    return messages