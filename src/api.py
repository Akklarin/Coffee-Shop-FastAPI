from fastapi import APIRouter
from users.views import user_router
from auth.views import auth_router


main_router = APIRouter()
main_router.include_router(user_router)
main_router.include_router(auth_router)
