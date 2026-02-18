from sqlalchemy.orm import Session
from app.repositories.internship_form_field_repository import (
    InternshipFormFieldRepository,
)
from app.repositories.internship_repository import InternshipRepository
from app.repositories.application_repository import ApplicationRepository
from app.core.exceptions import PermissionDenied, NotFoundError, ConflictError
from app.models.internship_form_field import InternshipFormField


class InternshipFormService:

    def __init__(self):
        self.repo = InternshipFormFieldRepository()
        self.internship_repo = InternshipRepository()
        self.application_repo = ApplicationRepository()

    def create_form_fields(self, db: Session, employer, internship_id: int, payload):

        # 1️⃣ Validate internship exists
        internship = self.internship_repo.get_by_id(db, internship_id)
        if not internship:
            raise NotFoundError("Internship not found")

        # 2️⃣ Validate employer role
        if employer.role != "employer":
            raise PermissionDenied("Only employers can modify form fields")

        # 3️⃣ Validate ownership
        if internship.employer_id != employer.id:
            raise PermissionDenied("Not allowed")

        # 4️⃣ Internship must be open
        if internship.status != "open":
            raise ConflictError("Cannot modify form of closed internship")

        # 5️⃣ Cannot modify after applications exist
        existing_apps = self.application_repo.list_by_internship(db, internship_id)
        if existing_apps:
            raise ConflictError("Cannot modify form after applications exist")

        # 6️⃣ Check duplicate keys inside payload
        incoming_keys = [field.field_key for field in payload.fields]
        if len(incoming_keys) != len(set(incoming_keys)):
            raise ConflictError("Duplicate field_key in request")

        # 7️⃣ Check duplicate keys in DB
        for key in incoming_keys:
            existing_key = self.repo.get_by_key(db, internship_id, key)
            if existing_key:
                raise ConflictError(f"Field key '{key}' already exists")

        created_fields = []

        try:
            for field_data in payload.fields:
                field = InternshipFormField(
                    internship_id=internship_id,
                    field_key=field_data.field_key,
                    label=field_data.label,
                    field_type=field_data.field_type,
                    is_required=field_data.is_required,
                )
                db.add(field)
                created_fields.append(field)

            db.commit()

            for f in created_fields:
                db.refresh(f)

            return created_fields

        except Exception:
            db.rollback()
            raise

    def list_form_fields(self, db: Session, internship_id: int):
        internship = self.internship_repo.get_by_id(db, internship_id)
        if not internship:
            raise NotFoundError("Internship not found")

        return self.repo.list_by_internship(db, internship_id)
