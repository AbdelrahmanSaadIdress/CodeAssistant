from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Body, Depends

from controllers import ProjectUploadController, ProjectFilesController
from helpers import get_settings, Settings

import os

upload_router = APIRouter(
    prefix="/api/v1/projects",
    tags=["Projects"],
)


# ── Dependencies ────────────────────────────────────────────────────

def get_upload_controller() -> ProjectUploadController:
    return ProjectUploadController()


def get_files_controller(settings: Settings = Depends(get_settings)) -> ProjectFilesController:
    return ProjectFilesController(
        embedding_api_key = settings.OPENAI_API_KEY,
        embedding_api_url = getattr(settings, "OPENAI_API_URL", None),
    )


# ── Routes ──────────────────────────────────────────────────────────

@upload_router.post("/upload")
async def upload_project(
    background_tasks:  BackgroundTasks,
    project_id:        str        = Body(..., embed=True),
    file:              UploadFile = File(...),
    upload_controller: ProjectUploadController = Depends(get_upload_controller),
    files_controller:  ProjectFilesController  = Depends(get_files_controller),
):
    """
    Upload a RAR file for a project.
    Extracts the archive and indexes all Python files into the project
    vector DB in the background.
    """

    # Step 1: Save RAR to disk
    rar_path = await upload_controller.save_rar(project_id, file)

    # Step 2: Extract + chunk + embed in background
    background_tasks.add_task(
        _extract_and_index,
        upload_controller,
        files_controller,
        rar_path,
        project_id,
    )

    return {
        "message":    "Project uploaded successfully. Indexing in progress.",
        "project_id": project_id,
        "status":     "indexing",
        "files_path": os.path.join(str(upload_controller.base_dir), project_id, "files"),
    }


@upload_router.delete("/{project_id}")
async def delete_project(
    project_id:       str,
    files_controller: ProjectFilesController = Depends(get_files_controller),
):
    """Wipe all vectors for a project. Call before re-uploading a new version."""
    files_controller._embedder.delete_project(project_id)

    return {
        "message":    f"Project '{project_id}' vectors deleted successfully.",
        "project_id": project_id,
    }


@upload_router.get("/{project_id}/status")
async def project_index_status(
    project_id:       str,
    files_controller: ProjectFilesController = Depends(get_files_controller),
):
    """Check how many chunks are currently indexed for a project."""
    count = files_controller.chunk_count(project_id)

    return {
        "project_id":   project_id,
        "total_chunks": count,
        "indexed":      count > 0,
    }


# ── Background task ─────────────────────────────────────────────────

def _extract_and_index(
    upload_controller: ProjectUploadController,
    files_controller:  ProjectFilesController,
    rar_path,
    project_id: str,
):
    """
    Runs after upload completes:
        extract RAR  →  load files  →  chunk  →  embed  →  ChromaDB
    """
    upload_controller.extract_rar(rar_path, project_id)
    total = files_controller.index_project(project_id)
    print(f"[upload] project='{project_id}' → {total} chunks indexed.")
