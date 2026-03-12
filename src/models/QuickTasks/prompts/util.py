
def _format_rag_sections(state) -> str:
    """
    Renders both RAG sources into a clean, labeled block
    that is injected into every prompt that benefits from context.
    """
    project_docs  = state.retrieval_context.documents
    codebase_docs = state.codebase_context.documents

    sections = []

    if project_docs:
        sections.append("### Project Context (from user's uploaded files)")
        sections.append("\n---\n".join(project_docs))

    if codebase_docs:
        sections.append("### Codebase Reference (from curated GitHub repos)")
        sections.append("\n---\n".join(codebase_docs))

    if not sections:
        return "No additional context available."

    return "\n\n".join(sections)
