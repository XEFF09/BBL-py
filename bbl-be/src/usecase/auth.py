import uuid
import hashlib
from typing import Protocol, Optional, Dict, Any
from datetime import datetime, timedelta
from jose import jwt
from pydantic import BaseModel

from domain.user import User

SECRET_KEY = "kawldlkj1odjko1jdkwqjdqw"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class TokenData(BaseModel):
    username: Optional[str] = None
    is_admin: bool = False


class AuthUsecase(Protocol):
    async def login(self, req: User) -> str: ...


class UserService:
    def __init__(self):
        self.users_db: Dict[str, Dict[str, Any]] = {}
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
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encoded_jwt
