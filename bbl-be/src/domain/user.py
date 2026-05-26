from typing import TypedDict


class User(TypedDict):
    username: str
    password: str
    is_admin: bool
