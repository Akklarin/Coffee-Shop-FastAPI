from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Schema for user registration."""
    # Here it makes sense to add a restriction: prohibit the use of Cyrillic characters in the email and password.
    email: EmailStr
    password: str = Field(min_length=6)
    first_name: str | None = None
    last_name: str | None = None


class UserLogin(BaseModel):
    """Schema for user login request."""
    email: EmailStr
    password: str


class TokenPair(BaseModel):
    """Schema representing an access/refresh token pair."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    """Refresh token used to request a new access token"""
    refresh_token: str


class VerifyUser(BaseModel):
    """Schema used to verify user email with a verification code."""
    email: EmailStr
    code: str
