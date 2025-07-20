from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_session

# Dependency for injecting the database session into endpoints
SessionDep = Annotated[AsyncSession, Depends(get_session)]
