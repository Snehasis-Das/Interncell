from pydantic import BaseModel
from app.enums.form_field_type import FormFieldType


class FormFieldCreate(BaseModel):
    field_key: str
    label: str
    field_type: FormFieldType
    is_required: bool


class FormFieldResponse(BaseModel):
    id: int
    field_key: str
    label: str
    field_type: FormFieldType
    is_required: bool

    class Config:
        from_attributes = True
        
class FormFieldBulkCreate(BaseModel):
    fields: list[FormFieldCreate]

