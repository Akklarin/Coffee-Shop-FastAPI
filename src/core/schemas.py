from pydantic import BaseModel


class TokenData(BaseModel):
    """Schema for data extracted from a validated JWT token."""
    sub: str
    role: str
