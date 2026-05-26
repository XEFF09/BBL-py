from fastapi import FastAPI, APIRouter, HTTPException, status, Body

from domain.user import User
from usecase.auth import UserService


auth_service = UserService()

app = FastAPI()
api_router = APIRouter(prefix="/api")
auth_router = APIRouter(prefix="/auth", tags=["auth"])
booking_router = APIRouter(prefix="/bookings", tags=["bookings"])


@auth_router.post("/login")
async def login(username: str = Body(...), password: str = Body(...)):
    try:
        payload: User = {
            "username": username,
            "password": password,
            "is_admin": False,
        }
        result = await auth_service.login(payload)
        return {"access_token": result}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
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
