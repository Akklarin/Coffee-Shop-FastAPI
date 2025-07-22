from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends

from src.users.dependencies import SessionDep
from .service import get_all_users, get_user_by_id, get_current_user
from .schemas import UserOut
from .dependencies import AdminOnly
from src.users.models import User

user_router = APIRouter(tags=["User_management"])


@user_router.get("/me", response_model=UserOut)
async def get_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@user_router.get("/", response_model=list[UserOut])
async def all_users(session: SessionDep, admin: AdminOnly):
    return await get_all_users(session)


@user_router.get("/{user_id}", response_model=UserOut)
async def user_by_id(user_id: int, session: SessionDep, admin: AdminOnly):
    user = await get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.patch("/users/{id}")
async def patch_user():
    pass


@user_router.delete("/users/{id}")
async def delete_user():
    pass
