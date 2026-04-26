from fastapi import FastAPI
from helpers import get_settings, Settings

from routes import base_router, upload_router, quick_tasks_router, codebase_router




app = FastAPI()
app.include_router(base_router)
app.include_router(upload_router)
app.include_router(quick_tasks_router)
app.include_router(codebase_router)



# from huggingface_hub import login, upload_folder

# hf_token = "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"
# login(token=hf_token)

# print("fffffffff")

# # Push your model files

# upload_folder(folder_path=".", repo_id="AbdoSaad24/deepseek-coder-6.7b-code-gen-finetuned", repo_type="model")

# print("fffffffff")