"""Application configuration using Pydantic settings."""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os


class Settings(BaseSettings):
    """Application settings."""

    # App
    APP_NAME: str = "Swedish NewsDiff Tracker"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./newsdiff.db"

    # CORS - can be set as JSON string in env var
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Scraping
    USER_AGENT: str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    # Logging
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        # Don't try to load .env file in production
        env_file=".env" if os.path.exists(".env") else None,
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


# Initialize settings - will read from environment variables
settings = Settings()
