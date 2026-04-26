from fastapi import FastAPI
from helpers import get_settings, Settings

from routes import base_router, upload_router, quick_tasks_router, codebase_router




app = FastAPI()
app.include_router(base_router)
app.include_router(upload_router)
app.include_router(quick_tasks_router)
app.include_router(codebase_router)



