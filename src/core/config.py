from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
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

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )


settings = Settings()


def get_db_url():
    return (f'postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@'
            f'{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}')