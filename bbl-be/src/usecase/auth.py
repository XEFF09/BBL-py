import hashlib
from typing import Dict
from datetime import datetime, timedelta
from jose import jwt
from domain.dto.auth import AuthRequest
from domain.user import User
from config.config import Config


class AuthService:
    def __init__(self, cfg: Config):
        self.users_db: Dict[str, User] = {}
        self.jwt_cfg = cfg["jwt"]
        self._init_users()

    def _init_users(self):
        admin_user: User = {
            "username": "admin",
            "password": self._hash_password("admin123"),
            "is_admin": True,
        }
        self.users_db[admin_user["username"]] = admin_user

    async def register(self, req: AuthRequest):
        if req.username in self.users_db:
            raise ValueError("Username already exists")

        self.users_db[req.username] = {
            "username": req.username,
            "password": self._hash_password(req.password),
            "is_admin": False,
        }

    async def login(self, req: AuthRequest) -> str:
        user = self.users_db.get(req.username)

        if not user:
            raise ValueError("Invalid username or password")

        hash_req_password = hashlib.sha256(req.password.encode()).hexdigest()
        hash_user_password = user["password"]

        if not hash_req_password == hash_user_password:
            raise ValueError("Invalid username or password")

        access_token = self._create_access_token(
            data={
                "username": user["username"],
                "is_admin": user["is_admin"],
            }
        )
        return access_token

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def _create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.jwt_cfg["expire_minutes"])
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, self.jwt_cfg["secret_key"], algorithm=self.jwt_cfg["algorithm"]
        )

        return encoded_jwt
