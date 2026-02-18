from pydantic import BaseModel
from datetime import datetime
from app.enums.application_status import ApplicationStatus
from typing import Dict,List


class ApplicationAnswerResponse(BaseModel):
    field_key: str
    label: str
    value: str

    class Config:
        from_attributes = True

class ApplicationResponse(BaseModel):
    id: int
    user_id: int
    internship_id: int
    status: ApplicationStatus
    created_at: datetime
    answers: List[ApplicationAnswerResponse]

    class Config:
        from_attributes = True


class ApplicationStatusUpdate(BaseModel):
    status: ApplicationStatus

class ApplicationCreate(BaseModel):
    answers: Dict[str, str]
