import uuid
from fastapi import Depends, FastAPI, APIRouter, HTTPException, status, Body
from fastapi.middleware.cors import CORSMiddleware

from domain.booking import Booking
from domain.dto.auth import AuthRequest
from domain.dto.booking import CreateBookingRequest
from internal.adapter.db.mock.user import MockUser
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

init_mock_user = MockUser()
mock_users_db = init_mock_user.get_instance()

auth_service = AuthService(cfg, mock_users_db)
booking_service = BookingService(mock_users_db)

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
async def make_appointment(
    req: CreateBookingRequest, curr_user=Depends(auth_middleware.validate)
):
    try:
        await booking_service.make_appointment(req, curr_user)
        return {"message": "Appointment created successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@booking_router.get("/")
async def get_appointments(curr_user=Depends(auth_middleware.validate)):
    try:
        appointments = await booking_service.get_appointments(curr_user)
        return {"message": "Appointments retrieved successfully", "data": appointments}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@booking_router.get("/{id}")
async def get_appointment(id: str, curr_user=Depends(auth_middleware.validate)):
    try:
        appointment = await booking_service.get_appointment(id, curr_user)
        return {"message": "Appointment retrieved successfully", "data": appointment}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@booking_router.delete("/{id}")
async def cancel_appointment(id: str, curr_user=Depends(auth_middleware.validate)):
    try:
        await booking_service.cancel_appointment(id, curr_user)
        return {"message": "Appointment cancelled successfully"}
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
