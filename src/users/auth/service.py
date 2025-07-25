import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from src.users.models import User, ValidationCode
from src.core.security import hash_password, create_access_token, create_refresh_token, decode_token
from .schemas import UserCreate, UserLogin, TokenPair, VerifyUser
from .utils import generate_verification_code


async def create_user(user_data: UserCreate, db: AsyncSession):
    """Register a new user and create a verification code."""
    result = await db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    verification_code = generate_verification_code()
    print(f"Verification code for {user_data.email}: {verification_code}")

    new_user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        is_verified=False,
        role="user"
    )
    db.add(new_user)

    validation = ValidationCode(email=user_data.email, code=verification_code)
    db.add(validation)

    await db.commit()
    await db.refresh(new_user)
    return new_user


async def authenticate_user(user_data: UserLogin, db: AsyncSession) -> TokenPair:
    """Authenticate user credentials and return a token pair."""
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
    """Generate a new access token using a valid refresh token."""
    token_data = decode_token(refresh_token, expected_type="refresh")
    new_access_token = create_access_token({"sub": token_data.sub, "role": token_data.role})
    return new_access_token


async def verify_user(data: VerifyUser, db: AsyncSession):
    """Mark user as verified if the provided code matches."""
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_verified:
        raise HTTPException(status_code=400, detail="User already verified")

    result = await db.execute(select(ValidationCode).where(ValidationCode.email == data.email))
    validation = result.scalar_one_or_none()
    if not validation:
        raise HTTPException(status_code=400, detail="No verification code found")

    if validation.code != data.code:
        raise HTTPException(status_code=400, detail="Invalid verification code")

    await db.delete(validation)
    user.is_verified = True
    await db.commit()
    return {"message": "User verified successfully"}
