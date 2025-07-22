from fastapi import APIRouter

from src.users.user_management.views import user_router
from src.users.auth.views import auth_router


main_router = APIRouter()
main_router.include_router(user_router)
main_router.include_router(auth_router)
