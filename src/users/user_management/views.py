from fastapi import APIRouter

user_router = APIRouter(tags=["User_management"])


@user_router.get("/me")
async def get_current_user():
    pass


@user_router.get("/users")
async def get_all_users():
    pass


@user_router.get("/users/{id}")
async def get_user_by_id():
    pass


@user_router.patch("/users/{id}")
async def patch_user():
    pass


@user_router.delete("/users/{id}")
async def delete_user():
    pass
