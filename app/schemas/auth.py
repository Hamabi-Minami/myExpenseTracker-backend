from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class LoginRequest(BaseModel):
    account: str = Field(..., min_length=4, max_length=50)
    password: str = Field(..., min_length=6, max_length=128)


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    username: str


class UserCreate(BaseModel):
    username: str
    account: str = Field(..., min_length=4, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
