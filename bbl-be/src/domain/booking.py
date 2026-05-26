from typing import TypedDict


class Booking(TypedDict):
    _id: str
    topic: str
    from_time: str
    to_time: str
    creator_username: str
    participants: list[str]
