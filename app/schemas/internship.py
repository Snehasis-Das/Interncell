from pydantic import BaseModel, Field
from datetime import datetime
from app.schemas.internship_form_field import FormFieldResponse
from app.enums.internship_status import (
    InternshipStatus,
    InternshipWorkMode,
    InternshipTiming,
)


class InternshipCreate(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=10)

    details: str | None = None
    location: str | None = None
    work_mode: InternshipWorkMode | None = None
    timing: InternshipTiming | None = None
    experience_min_years: int | None = None
    duration_weeks: int | None = None
    stipend_amount: int | None = None
    stipend_currency: str | None = None
    application_deadline: datetime | None = None

class InternshipUpdate(BaseModel):
    pass
    '''
    title: str | None = None
    description: str | None = None
    status: InternshipStatus | None = None
    '''

class InternshipResponse(BaseModel):
    id: int
    title: str
    description: str
    details: str | None
    location: str | None
    work_mode: InternshipWorkMode | None
    timing: InternshipTiming | None
    experience_min_years: int | None
    duration_weeks: int | None
    stipend_amount: int | None
    stipend_currency: str | None
    application_deadline: datetime | None

    status: InternshipStatus
    employer_id: int
    created_at: datetime
    form_fields: list[FormFieldResponse] = []

    class Config:
        from_attributes = True
