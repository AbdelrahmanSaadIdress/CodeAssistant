from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # App
    APP_NAME:    str = "Code Assistant Chatbot"
    APP_VERSION: str = "0.1"

    PROVIDERS: str = "openai"

    HF_Generation_MODEL_ID: str = ""
    HF_Autocomplete_MODEL_ID: str = ""
    HF_Audit_MODEL_ID: str = ""

    # LLM + Embeddings
    OPENAI_API_KEY: str
    OPENAI_API_URL: str = "https://models.github.ai/inference"
    OPENAI_MODEL_ID: str = "openai/gpt-4o-mini"


    # Storage paths
    CHROMA_PERSIST_DIR: str = "assets/vector_store"
    PROJECTS_BASE_DIR:  str = "assets/projects"
    CODEBASE_REPOS_DIR: str = "assets/codebase/repos"
    OUTPUT_BASE_DIR:    str = "assets/output"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()