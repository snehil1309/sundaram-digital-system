from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

class LoginRequest(BaseModel):
    username: str
    password: str

router = APIRouter()

@router.post("/login")
def login(request: LoginRequest):
    if request.username == "admin" and request.password == "admin123":
        return {"message": "Login successful", "token": "fake-jwt-token"}
    raise HTTPException(status_code=401, detail="Invalid credentials")
