from fastapi import APIRouter, HTTPException, Depends

from src.users.dependencies import SessionDep
from .service import get_all_users, get_user_by_id, get_current_user, delete_user_by_id, update_user
from .schemas import UserOut, UserUpdate
from .dependencies import AdminOnly
from src.users.models import User

user_router = APIRouter(tags=["User_management"])


@user_router.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@user_router.get("/users/", response_model=list[UserOut])
async def all_users(session: SessionDep, admin: AdminOnly):
    return await get_all_users(session)


@user_router.get("/users/{user_id}", response_model=UserOut)
async def user_by_id(user_id: int, session: SessionDep, admin: AdminOnly):
    user = await get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int, session: SessionDep, admin: AdminOnly):
    user = await get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await delete_user_by_id(session, user_id)


@user_router.patch("/users/{user_id}", response_model=UserOut)
async def patch_user(
    user_id: int,
    data: UserUpdate,
    session: SessionDep,
    admin: AdminOnly
):

    return await update_user(session, user_id, data)
