from fastapi import APIRouter, HTTPException

from .schemas import UserCreate, TokenPair, UserLogin, RefreshTokenRequest
from .service import create_user, authenticate_user, refresh_access_token
from src.users.dependencies import SessionDep


auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/signup", response_model=None, status_code=201)
async def signup(user: UserCreate, db: SessionDep):
    await create_user(user, db)


@auth_router.post("/login", response_model=TokenPair)
async def login_user(user_data: UserLogin, db: SessionDep):
    return await authenticate_user(user_data, db)


@auth_router.post("/refresh", response_model=TokenPair)
async def refresh_token(request: RefreshTokenRequest):
    try:
        new_access_token = await refresh_access_token(request.refresh_token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    return {
        "access_token": new_access_token,
        "refresh_token": request.refresh_token,
        "token_type": "bearer"
    }
