from pydantic import BaseModel, EmailStr, Field
from app.enums.roles import UserRole


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    role: UserRole


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
