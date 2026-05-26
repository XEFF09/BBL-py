import uuid
from fastapi import Depends, FastAPI, APIRouter, HTTPException, status, Body
from fastapi.middleware.cors import CORSMiddleware

from domain.booking import Booking
from domain.dto.auth import AuthRequest
from middleware.auth import AuthMiddleware
from usecase.auth import AuthService
from usecase.booking import BookingService
from config.config import cfg

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

auth_service = AuthService(cfg)
booking_service = BookingService()

api_router = APIRouter(prefix="/api")
auth_router = APIRouter(prefix="/auth", tags=["auth"])
booking_router = APIRouter(prefix="/bookings", tags=["bookings"])

auth_middleware = AuthMiddleware(cfg)


@auth_router.post("/login")
async def login(req: AuthRequest):
    try:
        result = await auth_service.login(req)
        return {
            "message": "Login successful",
            "access_token": result,
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@auth_router.post("/register")
async def register(req: AuthRequest):
    try:
        await auth_service.register(req)
        return {
            "message": "Registration successful",
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@booking_router.post("/")
async def make_appointment(req: dict, current_user=Depends(auth_middleware.validate)):
    booking_id = str(uuid.uuid4())
    booking: Booking = {
        "_id": booking_id,
        "topic": req["topic"],
        "from_time": req["from_time"],
        "to_time": req["to_time"],
        "creator_username": req["creator_username"],
        "participants": req.get("participants", []),
    }
    try:
        await booking_service.make_appointment(booking)
        return {"message": "Appointment created successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@booking_router.get("/")
async def get_appointments(current_user=Depends(auth_middleware.validate)):
    try:
        appointments = await booking_service.get_appointments(current_user)
        return {"message": "Appointments retrieved successfully", "data": appointments}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@api_router.get("/")
def welcome():
    return {"message": "Welcome to the Booking API!"}


api_router.include_router(auth_router)
api_router.include_router(booking_router)
app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
    )
