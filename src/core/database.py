"""
This module configures the asynchronous SQLAlchemy engine, sessionmaker, and
base declarative class for use throughout the application.
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from .config import get_db_url


DATABASE_URL = get_db_url()

engine = create_async_engine(DATABASE_URL, future=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()


async def get_session() -> AsyncSession:
    """Provides a scoped asynchronous database session."""
    async with AsyncSessionLocal() as session:
        yield session
