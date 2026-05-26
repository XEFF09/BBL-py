from typing import Optional
from fastapi import HTTPException, status, Header
from pydantic import BaseModel
from jose import jwt
from config.config import Config


class TokenData(BaseModel):
    username: Optional[str] = None
    is_admin: bool = False


class AuthMiddleware:
    def __init__(self, cfg: Config):
        self.jwt_cfg = cfg["jwt"]

    async def _verify_token(self, token: str) -> Optional[TokenData]:
        try:
            payload = jwt.decode(
                token,
                self.jwt_cfg["secret_key"],
                algorithms=[self.jwt_cfg["algorithm"]],
            )
            username: str = payload["username"]
            is_admin: bool = payload.get("is_admin", False)
            return TokenData(username=username, is_admin=is_admin)
        except Exception:
            return None

    async def validate(self, authorization: str = Header(None)):
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

        token_data = await self._verify_token(token)
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )

        return {
            "username": token_data.username,
            "is_admin": token_data.is_admin,
        }
