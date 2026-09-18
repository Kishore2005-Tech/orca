from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.

    Environment variables can be supplied through a .env file
    or directly through the process environment.
    """

    app_name: str = "ORCA API"
    app_version: str = "1.0.0"
    app_description: str = (
        "Oceanic Reasoning & Coastal Advisory API"
    )

    environment: str = "development"
    debug: bool = True

    host: str = "0.0.0.0"
    port: int = 8000

    # Frontend origins allowed to call the API.
    cors_origins: List[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ]
    )

    # API behavior
    api_prefix: str = "/api/v1"

    request_timeout_seconds: float = 30.0

    # Maximum accepted query size.
    max_query_length: int = 5000

    # Coordinator behavior
    enable_conversation_context: bool = True

    # Verification is enabled by default.
    enable_verification: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return a cached Settings instance.

    Using a cached configuration prevents repeatedly reading
    environment variables during API requests.
    """
    return Settings()
