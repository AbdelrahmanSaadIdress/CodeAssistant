from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # App
    APP_NAME:    str = "Code Assistant Chatbot"
    APP_VERSION: str = "0.1"

    # LLM + Embeddings
    OPENAI_API_KEY: str
    OPENAI_API_URL: str = "https://models.github.ai/inference"

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