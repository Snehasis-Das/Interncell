from sqlalchemy.orm import Session
from app.models.internship_form_field import InternshipFormField


class InternshipFormFieldRepository:

    def create(self, db: Session, internship_id: int, payload):
        field = InternshipFormField(
            internship_id=internship_id,
            field_key=payload.field_key,
            label=payload.label,
            field_type=payload.field_type.value,
            is_required=payload.is_required,
        )
        db.add(field)
        return field

    def list_by_internship(self, db: Session, internship_id: int):
        return (
            db.query(InternshipFormField)
            .filter(InternshipFormField.internship_id == internship_id)
            .all()
        )

    def get_by_key(self, db: Session, internship_id: int, field_key: str):
        return (
            db.query(InternshipFormField)
            .filter(
                InternshipFormField.internship_id == internship_id,
                InternshipFormField.field_key == field_key,
            )
            .first()
        )
