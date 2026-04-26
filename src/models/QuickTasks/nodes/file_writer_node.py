"""
file_writer_node.py
-------------------
Final node in the graph. After refining, asks the LLM to decide
how many files the code should be split into, then writes each file
to disk under:

    assets/output/{project_id}/{file_name}

State is updated with the list of written file paths.
"""

import os
from pathlib import Path

from models.QuickTasks.states import AgentState, FileSplitResult, OutputFile
from models.QuickTasks.prompts.file_split_prompt import build_file_split_messages
from stores.llm.llm_util import call_llm
from langchain_core.runnables import RunnableConfig


OUTPUT_BASE_DIR = "assets/output"


def file_writer_node(
    state:  AgentState,
    llm_config,
) -> AgentState:
    print("── FILE WRITER NODE ──")

    # ── 1. Ask LLM to decide split strategy ───────────────────────
    messages = build_file_split_messages(state)
    result   = call_llm(llm_config, messages)

    try:
        parsed = FileSplitResult(**result)
    except Exception as exc:
        print(f"[file_writer] FileSplitResult parse error: {exc} — falling back to single file.")
        parsed = _fallback_single_file(state)

    # ── 2. Write files to disk ─────────────────────────────────────
    project_id = state.project_id or "default"
    output_dir = Path(OUTPUT_BASE_DIR) / project_id
    output_dir.mkdir(parents=True, exist_ok=True)

    written: list[OutputFile] = []

    for file_entry in parsed.files:
        file_path = output_dir / file_entry.file_name
        file_path.write_text(file_entry.content, encoding="utf-8")
        written.append(OutputFile(
            file_name = file_entry.file_name,
            file_path = str(file_path),
            content   = file_entry.content,
        ))
        print(f"[file_writer] wrote → {file_path}")

    # ── 3. Update state ────────────────────────────────────────────
    state.output_files = written

    return state


# ── Fallback ────────────────────────────────────────────────────────

def _fallback_single_file(state: AgentState) -> FileSplitResult:
    """
    Used when the LLM returns unparseable output.
    Saves everything as a single 'output.py'.
    """
    from models.QuickTasks.states import FileEntry
    return FileSplitResult(files=[
        FileEntry(
            file_name = "output.py",
            content   = state.last_code or state.result or "",
        )
    ])
