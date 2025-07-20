from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from .config import settings
from .schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def decode_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        sub = payload.get("sub")
        role = payload.get("role")
        if sub is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return TokenData(sub=sub, role=role)
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
