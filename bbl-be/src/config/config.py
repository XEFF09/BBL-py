from typing import TypedDict
from dotenv import load_dotenv
import os

load_dotenv()


class JWTConfig(TypedDict):
    secret_key: str
    algorithm: str
    expire_minutes: int


class Config(TypedDict):
    jwt: JWTConfig


cfg: Config = {
    "jwt": {
        "secret_key": str(os.getenv("SECRET_KEY")),
        "algorithm": str(os.getenv("ALGORITHM")),
        "expire_minutes": int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)),
    }
}
