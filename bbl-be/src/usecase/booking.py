from datetime import datetime
import uuid
from typing import Dict, Optional, List

from domain.booking import Booking
from domain.dto.booking import CreateBookingRequest


class BookingService:
    def __init__(self, mock):
        self.bookings: Dict[str, Booking] = {}
        self.mock = mock

    def _time_parser(self, time_str: str):
        try:
            dt = datetime.strptime(time_str.strip().lower(), "%I:%M%p").time()
            return dt
        except ValueError:
            raise ValueError("Invalid time format. Expected format: HH:MMAM/PM")

    async def make_appointment(
        self, req: CreateBookingRequest, curr_user: dict
    ) -> dict:
        from_time = self._time_parser(req.from_time)
        to_time = self._time_parser(req.to_time)

        if from_time >= to_time:
            raise ValueError("from_time must be before to_time")

        if curr_user.get("username", None) is None:
            raise ValueError("Unable to identify user")

        if any([user for user in req.participants if user not in self.mock]):
            raise ValueError("One or more participants do not exist")

        booking_id = str(uuid.uuid4())
        booking: Booking = {
            "_id": booking_id,
            "topic": req.topic,
            "from_time": from_time,
            "to_time": to_time,
            "author": curr_user["username"],
            "participants": req.participants,
        }
        self.bookings[booking["_id"]] = booking
        return dict(booking)

    async def get_appointments(self, curr_user: dict) -> List[Booking]:
        if curr_user.get("is_admin", False):
            return list(self.bookings.values())
        return [
            b for b in self.bookings.values() if b["author"] == curr_user["username"]
        ]

    async def get_appointment(self, id: str, curr_user: dict) -> Optional[Booking]:
        booking = self.bookings.get(id, None)
        if booking is None:
            raise ValueError("Booking not found")

        if curr_user.get("is_admin", False):
            return booking

        if booking["author"] != curr_user["username"]:
            raise ValueError("Unauthorized to view this booking")

        return booking

    async def cancel_appointment(self, id: str, curr_user: dict) -> dict:
        booking = self.bookings.get(id, None)
        if booking is None:
            raise ValueError("Booking not found")

        if curr_user.get("is_admin", False):
            del self.bookings[id]
            return {"message": "Booking cancelled"}

        if booking["author"] != curr_user["username"]:
            raise ValueError("Unauthorized to view this booking")

        del self.bookings[id]
        return {"message": "Booking cancelled"}
