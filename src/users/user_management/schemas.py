from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserOut(BaseModel):
    id: int
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    role: str
    is_verified: bool
    created_at: datetime

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
