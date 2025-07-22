import bcrypt
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta, UTC

from .config import settings
from .schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def create_access_token(data: dict) -> str:
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    to_encode.update({
        "type": "access",
        "exp": datetime.now(UTC) + expires_delta
    })
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(data: dict) -> str:
    expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = data.copy()
    to_encode.update({
        "type": "refresh",
        "exp": datetime.now(UTC) + expires_delta
    })
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str, expected_type: str = None) -> TokenData:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        sub = payload.get("sub")
        role = payload.get("role")
        token_type = payload.get("type")

        if sub is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        if expected_type and token_type != expected_type:
            raise HTTPException(status_code=401, detail=f"Expected a {expected_type} token")

        return TokenData(sub=sub, role=role)
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
