import uuid
import hashlib
from typing import Protocol, Optional, Dict, Any
from datetime import datetime, timedelta
from jose import jwt
from pydantic import BaseModel
from domain.user import User
from dotenv import load_dotenv
import os

load_dotenv()

secret_key = str(os.getenv("SECRET_KEY"))
algo = str(os.getenv("ALGORITHM"))
exp = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


class TokenData(BaseModel):
    username: Optional[str] = None
    is_admin: bool = False


class AuthUsecase(Protocol):
    async def login(self, req: User) -> str: ...


class UserService:
    def __init__(self):
        self.users_db = {}
        self._init_users()

    def _init_users(self):
        admin_user = {
            "user_id": str(uuid.uuid4()),
            "username": "admin",
            "password_hash": self.hash_password("admin123"),
            "is_admin": True,
        }
        regular_user = {
            "user_id": str(uuid.uuid4()),
            "username": "user",
            "password_hash": self.hash_password("user123"),
            "is_admin": False,
        }
        self.users_db[admin_user["username"]] = admin_user
        self.users_db[regular_user["username"]] = regular_user

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    async def login(self, payload: User) -> str:
        username = payload["username"]
        password = payload["password"]

        if username not in self.users_db:
            raise ValueError("Invalid username or password")

        user = self.users_db[username]

        if not hashlib.sha256(password.encode()).hexdigest() == user["password_hash"]:
            raise ValueError("Invalid username or password")

        access_token = self.create_access_token(
            data={
                "user_id": user["user_id"],
                "username": username,
                "is_admin": user["is_admin"],
            }
        )
        return access_token

    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=exp)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algo)

        return encoded_jwt

    def verify_token(self, token: str) -> Optional[TokenData]:
        try:
            payload = jwt.decode(token, secret_key, algorithms=[algo])
            username: str = payload["username"]
            is_admin: bool = payload.get("is_admin", False)
            return TokenData(username=username, is_admin=is_admin)
        except Exception:
            return None
