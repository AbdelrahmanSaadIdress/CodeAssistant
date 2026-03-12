import json
from models.QuickTasks.states import CodeGenerationResult
from .util import _format_rag_sections

def build_generate_messages(state) -> list:
    rag_section = _format_rag_sections(state)

    messages = [
        {
            "role": "system",
            "content": "\n".join([
                "You are a senior software engineer.",
                "",
                "Your task is to generate high-quality Python code.",
                "",
                "You will be given two types of reference context:",
                "1. Project Context — code from the user's own project.",
                "   Use this to match their coding style, naming conventions, and structure.",
                "2. Codebase Reference — real code from popular GitHub repositories.",
                "   Use this to follow idiomatic patterns for any libraries involved.",
                "",
                "Rules:",
                "- Follow best practices.",
                "- Write clean, readable, well-commented code.",
                "- Stay consistent with the user's project style when context is available.",
                "- Reference library patterns from the codebase context when relevant.",
                "- Return ONLY valid JSON matching the schema.",
                "- Do NOT include explanations outside the JSON.",
            ])
        },
        {
            "role": "user",
            "content": "\n".join([
                f"## Task\n{state.task or state.user_input}",
                "",
                f"## Existing Code\n{state.code_context.code or 'None'}",
                "",
                "## Retrieved Context",
                rag_section,
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

