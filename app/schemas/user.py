from pydantic import BaseModel
from app.enums.roles import UserRole
from datetime import datetime


class UserResponse(BaseModel):
    id: int
    email: str
    role: UserRole
    created_at: datetime

    class Config:
        from_attributes = True
