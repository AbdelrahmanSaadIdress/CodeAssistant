from fastapi import FastAPI
from helpers import get_settings, Settings

from routes import base_router, quick_tasks_router



from huggingface_hub import login
hf_token = "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"
login(token=hf_token)

app = FastAPI()
app.include_router(base_router)
app.include_router(quick_tasks_router)