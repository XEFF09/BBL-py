import uuid
from typing import Optional, List

from domain.booking import Booking


class BookingService:
    def __init__(self):
        self.bookings = {}

    async def make_appointment(self, booking: Booking) -> dict:
        self.bookings[booking["_id"]] = booking
        return dict(booking)

    async def get_appointments(self, current_user: dict) -> List[dict]:
        if current_user.get("is_admin"):
            return list(self.bookings.values())
        return [
            b
            for b in self.bookings.values()
            if b["creator_username"] == current_user["username"]
        ]

    async def get_appointment(self, booking_id: str) -> Optional[dict]:
        return self.bookings.get(booking_id)

    async def cancel_appointment(self, current_user: dict, booking_id: str) -> dict:
        if not current_user["is_admin"]:
            if booking_id not in self.bookings:
                raise ValueError("Booking not found")

            if (
                self.bookings[booking_id]["creator_username"]
                != current_user["username"]
            ):
                raise ValueError("Unauthorized to cancel this booking")

        del self.bookings[booking_id]
        return {"message": "Booking cancelled"}
