import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException


from src.users.models import User
from src.core.security import decode_token
from src.core.security import hash_password, create_access_token, create_refresh_token
from .schemas import UserCreate, UserLogin, TokenPair


async def create_user(user_data: UserCreate, db: AsyncSession):
    result = await db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        is_verified=False,
        role="user"
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def authenticate_user(user_data: UserLogin, db: AsyncSession) -> TokenPair:
    query = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    user = query.scalar_one_or_none()

    if not user or not bcrypt.checkpw(user_data.password.encode(), user.password_hash.encode()):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token_data = {"sub": str(user.id), "role": user.role}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return TokenPair(access_token=access_token, refresh_token=refresh_token)


async def refresh_access_token(refresh_token: str) -> str:
    token_data = decode_token(refresh_token, expected_type="refresh")
    new_access_token = create_access_token({"sub": token_data.sub, "role": token_data.role})
    return new_access_token
