from pydantic import BaseModel


class CreateBookingRequest(BaseModel):
    topic: str
    from_time: str
    to_time: str
    participants: list[str]
