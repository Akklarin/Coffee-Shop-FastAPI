from fastapi import APIRouter, HTTPException

from .schemas import UserCreate, TokenPair, UserLogin, RefreshTokenRequest, VerifyUser
from .service import create_user, authenticate_user, refresh_access_token, verify_user
from src.users.dependencies import SessionDep


auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post(
    "/signup",
    response_model=None,
    status_code=201,
    summary="Register a new user",
    description=(
        "Create a new user account in the system.  \n"
        "- **email** must be unique and valid.  \n"
        "- **password** will be hashed before storage.  \n"
        "- Optional fields: `first_name`, `last_name`.  \n\n"
        "After successful registration, the user will have `is_verified=False` "
        "and will need to complete email verification."
    ),
)
async def signup(user: UserCreate, db: SessionDep):
    await create_user(user, db)


@auth_router.post("/login", response_model=TokenPair,
    summary="Log in a user",
    description="Authenticates the user using email and password. Returns a new access and refresh token pair."
)
async def login_user(user_data: UserLogin, db: SessionDep):
    return await authenticate_user(user_data, db)


@auth_router.post("/refresh", response_model=TokenPair,
    summary="Refresh access token",
    description="Generates a new access token using a valid refresh token. The refresh token itself is reused."
)
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


@auth_router.post("/verify",
    summary="Verify user token",
    description="Verifies the provided token and checks if the associated user exists and is valid."
)
async def verify_user_route(data: VerifyUser, db: SessionDep):
    return await verify_user(data, db)
