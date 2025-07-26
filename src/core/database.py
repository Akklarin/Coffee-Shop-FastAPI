from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import get_async_db, get_db

# Async engine and session (for async API and async DB operations)
async_engine = create_async_engine(get_async_db(), future=True)
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)

# Synchronous engine and session (for Celery tasks and sync DB operations)
engine = create_engine(get_db(), future=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()


async def get_session() -> AsyncSession:
    """Provides a scoped asynchronous database session."""
    async with AsyncSessionLocal() as session:
        yield session
