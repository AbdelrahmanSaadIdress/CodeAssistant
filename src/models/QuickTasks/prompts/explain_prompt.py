from models.QuickTasks.states import CodeExplanationResult
import json

from .util import _format_rag_sections

def build_explain_messages(state) -> list:
    project_docs = state.retrieval_context.documents
    project_section = (
        "\n---\n".join(project_docs)
        if project_docs
        else "No project context available."
    )

    messages = [
        {
            "role": "system",
            "content": "\n".join([
                "You are an expert programming instructor.",
                "",
                "Explain the code clearly and accurately.",
                "",
                "You may be given Project Context — other files from the user's project.",
                "Use it to explain what imported functions or classes do when relevant.",
                "",
                "Rules:",
                "- Explain step by step.",
                "- Mention important concepts.",
                "- Reference project context only when it adds clarity.",
                "- Be concise.",
                "- Output only JSON.",
            ])
        },
        {
            "role": "user",
            "content": "\n".join([
                f"## Code to Explain\n{state.code_context.code or ''}",
                "",
                "## Project Context",
                project_section,
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

