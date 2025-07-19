from fastapi import APIRouter
from auth.schemas import UserCreate
from auth.service import create_user
from core.dependencies import SessionDep


auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/signup", response_model=None, status_code=201)
async def signup(user: UserCreate, db: SessionDep):
    await create_user(user, db)


@auth_router.post("/login")
async def login():
    pass


@auth_router.post("/refresh")
async def refresh():
    pass
