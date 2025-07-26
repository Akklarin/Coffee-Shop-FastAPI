from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr
from typing import Literal


class Settings(BaseSettings):
    """Configuration settings loaded from environment variables."""

    PROJECT_TITLE: str
    PROJECT_DESCRIPTION: str
    PROJECT_DOCS_URL: str
    PROJECT_HOST: str
    PROJECT_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    SECRET_KEY: str
    ALGORITHM: Literal["HS256", "RS256"] = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ADMIN_EMAIL: EmailStr
    ADMIN_PASSWORD: str

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )


settings = Settings()


def get_async_db():
    """
    Returns the database URL for asynchronous connections.

    This URL is used for the async API, async database operations,
    and most of the application logic that requires async support.
    """
    return (f'postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@'
            f'{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}')


def get_db():
    """
    Returns the database URL for synchronous connections.

    This URL is primarily used by Celery workers.
    """
    return (f'postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@'
            f'{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}')
