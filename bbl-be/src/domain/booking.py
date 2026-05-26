from datetime import time
from typing import TypedDict


class Booking(TypedDict):
    _id: str
    topic: str
    from_time: time
    to_time: time
    author: str
    participants: list[str]
