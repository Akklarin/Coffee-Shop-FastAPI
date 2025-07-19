from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models import User
from auth.schemas import UserCreate
from auth.utils import hash_password
from fastapi import HTTPException


async def create_user(user_data: UserCreate, db: AsyncSession):
    result = await db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        is_verified=False,
        role="user"
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
