from models.QuickTasks.states import BugDetectionResult
import json

from .util import _format_rag_sections

def build_bug_messages(state) -> list:
    # For bug detection, project context helps understand how helper
    # functions/imports are defined elsewhere in the project.
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
                "You are a senior debugging expert.",
                "",
                "Your task is to analyze code and detect bugs.",
                "",
                "You may be given Project Context — other files from the user's project.",
                "Use it to understand how imported functions, classes, or variables are defined.",
                "",
                "Rules:",
                "- Identify logical errors.",
                "- Identify syntax problems.",
                "- Identify misuse of project-internal functions if context reveals the correct signatures.",
                "- Suggest fixes.",
                "- Return JSON only.",
            ])
        },
        {
            "role": "user",
            "content": "\n".join([
                f"## Code to Debug\n{state.code_context.code or ''}",
                "",
                "## Project Context (other files in the same project)",
                project_section,
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

