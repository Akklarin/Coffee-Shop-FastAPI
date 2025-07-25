from typing import Annotated
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from src.users.models import User
from src.core.config import settings
from src.users.dependencies import SessionDep
from .schemas import UserUpdate


bearer_scheme = HTTPBearer()


async def get_current_user(
    session: SessionDep,
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
) -> User:
    """Returns the user extracted from a valid JWT access token"""
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = int(payload.get("sub"))
    except (JWTError, TypeError, ValueError):
        raise credentials_exception

    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise credentials_exception
    return user


async def get_current_admin(user: Annotated[User, Depends(get_current_user)]) -> User:
    """Ensures the current user has admin privileges"""
    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return user


async def get_all_users(session: AsyncSession) -> list[User]:
    """Fetches all users from the database"""
    result = await session.execute(select(User))
    return result.scalars().all()


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    """Retrieves a user by their ID"""
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def delete_user_by_id(session: AsyncSession, user_id: int) -> None:
    """Deletes a user by their ID"""
    stmt = delete(User).where(User.id == user_id)
    await session.execute(stmt)
    await session.commit()


async def update_user(session: AsyncSession, user_id: int, data: UserUpdate) -> User:
    """Updates user fields with provided data"""
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)

    await session.commit()
    await session.refresh(user)
    return user
