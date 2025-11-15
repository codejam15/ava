from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    FASTAPI_ENV: str
    APP_NAME: str = "AVA (Agile Virtual Assistant)"
    VERSION: str = "v1"
    PORT: int = 8000
    API_PREFIX: str = "/api/v1"
    ALLOWED_ORIGINS: List[str] = ["*"]
    ALLOWED_HOSTS: List[str] = ["*"]
    ALGORITHM: str = "HS256"
    LLM_MODEL: str = "gpt-4o"

    # Database Configuration
    DATABASE_URL: str

    # API Keys
    OPENAI_API_KEY: str

    model_config = SettingsConfigDict(
        env_file="./src/.env", env_file_encoding="utf-8", extra="ignore"
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
