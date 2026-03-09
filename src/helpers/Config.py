from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    APP_NAME:str
    APP_VERSION:str

    class Config:
        env_file = ".env"


def get_settings():
    return Settings()