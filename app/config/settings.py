from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    app_name: str = "AI Code Reviewer & Bug-Fixing Agent"
    app_version: str = "0.1.0"
    environment: str = "development"

    llm_provider: str = "openai"
    llm_model: str = ""

    embedding_provider: str = "openai"
    embedding_model: str = ""

    chroma_persist_directory: str = "./data/chroma"

    max_agent_iterations: int = 3

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()