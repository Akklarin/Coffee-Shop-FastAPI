import bcrypt
from fastapi import HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta, UTC

from .config import settings
from .schemas import TokenData


def hash_password(password: str) -> str:
    """Hashes a plain text password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def create_access_token(data: dict) -> str:
    """Generates a signed JWT access token with expiration.

    Args:
        data: A dictionary with user-related claims (e.g., 'sub', 'role').

    Returns:
        Encoded JWT access token as a string.
    """
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    to_encode.update({
        "type": "access",   # Explicitly mark token as an access token
        "exp": datetime.now(UTC) + expires_delta
    })
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(data: dict) -> str:
    """Generates a signed JWT refresh token with longer expiration.

    Args:
        data: A dictionary with user-related claims (e.g., 'sub', 'role').

    Returns:
        Encoded JWT refresh token as a string.
    """
    expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = data.copy()
    to_encode.update({
        "type": "refresh",  # Explicitly mark token as a refresh token
        "exp": datetime.now(UTC) + expires_delta
    })
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str, expected_type: str = None) -> TokenData:
    """Validates and decodes a JWT token, returning its contents.

    Args:
        token: JWT token as a string.
        expected_type: Optional string indicating whether a specific token type
                       (e.g., 'access' or 'refresh') is expected.

    Returns:
        TokenData containing the 'sub' and 'role' fields.

    Raises:
        HTTPException: If the token is invalid, malformed, or of the wrong type.
    """
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
