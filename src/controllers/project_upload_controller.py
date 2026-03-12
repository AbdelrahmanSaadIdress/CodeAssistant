import rarfile
from pathlib import Path
from fastapi import UploadFile, HTTPException


class ProjectUploadController:

    def __init__(self, base_dir: str = "assets/projects"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    async def save_rar(self, project_id: str, file: UploadFile):
        # Accept only .rar files
        if not file.filename.endswith(".rar"):
            raise HTTPException(status_code=400, detail="Only RAR files are allowed")

        project_folder = self.base_dir / project_id
        project_folder.mkdir(parents=True, exist_ok=True)

        rar_path = project_folder / file.filename

        content = await file.read()
        with open(rar_path, "wb") as f:
            f.write(content)

        return rar_path

    def extract_rar(self, rar_path: Path, project_id: str):
        # Validate RAR file
        try:
            rf = rarfile.RarFile(rar_path)
        except rarfile.Error:
            raise Exception("Uploaded file is not a valid RAR")
        extract_folder = self.base_dir / project_id / "files"

        extract_folder.mkdir(parents=True, exist_ok=True)

        rf.extractall(extract_folder)

        rf.close()

        return extract_folder