from typing import Optional
from fastapi import HTTPException, status, Header
from pydantic import BaseModel
from jose import jwt
from dotenv import load_dotenv
import os

load_dotenv()

secret_key = str(os.getenv("SECRET_KEY"))
algo = str(os.getenv("ALGORITHM"))
exp = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


class TokenData(BaseModel):
    username: Optional[str] = None
    is_admin: bool = False


def verify_token(token: str) -> Optional[TokenData]:
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algo])
        username: str = payload["username"]
        is_admin: bool = payload.get("is_admin", False)
        return TokenData(username=username, is_admin=is_admin)
    except Exception:
        return None


async def get_current_user(authorization: str = Header(None)):
    """Extract and verify JWT token from Authorization header."""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
        )

    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError("Invalid auth scheme")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
        )

    token_data = verify_token(token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return {
        "username": token_data.username,
        "is_admin": token_data.is_admin,
    }
