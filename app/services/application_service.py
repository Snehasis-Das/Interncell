from sqlalchemy.orm import Session

from app.repositories.application_repository import ApplicationRepository
from app.repositories.internship_repository import InternshipRepository
from app.repositories.upload_repository import UploadRepository

from app.core.exceptions import (
    PermissionDenied,
    NotFoundError,
    ConflictError,
)

from app.utils.validators import validate_application_status_transition
from app.adapters.factory import get_email_adapter,get_storage_adapter
from app.models.application_answer import ApplicationAnswer


class ApplicationService:

    def __init__(self):
        self.repo = ApplicationRepository()
        self.internship_repo = InternshipRepository()
        self.email_adapter = get_email_adapter()
        self.storage_adapter = get_storage_adapter()
        self.upload_repo = UploadRepository()
        
    # ===============================
    # APPLY TO INTERNSHIP
    # ===============================

    def apply_to_internship(
        self,
        db: Session,
        student,
        internship_id: int,
        payload,
    ):
        if student.role != "student":
            raise PermissionDenied("Only students can apply")

        internship = self.internship_repo.get_by_id(db, internship_id)
        if not internship:
            raise NotFoundError("Internship not found")

        if internship.status != "open":
            raise ConflictError("Internship is closed")

        existing = self.repo.get_by_user_and_internship(
            db,
            student.id,
            internship_id,
        )
        if existing:
            raise ConflictError("Already applied")

        # ---- Validate dynamic form ----
        form_fields = internship.form_fields

        required_keys = {
            field.field_key for field in form_fields if field.is_required
        }

        allowed_keys = {
            field.field_key for field in form_fields
        }

        submitted_keys = set(payload.answers.keys())

        missing = required_keys - submitted_keys
        if missing:
            raise ConflictError(f"Missing required fields: {missing}")

        unknown = submitted_keys - allowed_keys
        if unknown:
            raise ConflictError(f"Unknown fields submitted: {unknown}")

        # ---- Atomic Transaction ----
        try:
            application = self.repo.create(
                db=db,
                user_id=student.id,
                internship_id=internship_id,
            )
            
            db.flush()

            for field in form_fields:
                if field.field_key in payload.answers:

                    raw_value = payload.answers[field.field_key]

                    # ---- FILE FIELD HANDLING ----
                    if field.field_type == "file":

                        # Expect upload_id
                        try:
                            upload_id = int(raw_value)
                        except (TypeError, ValueError):
                            raise ConflictError(
                                f"Invalid upload_id for field '{field.field_key}'"
                            )

                        upload = self.upload_repo.get_by_id(db, upload_id)

                        if not upload:
                            raise ConflictError("Invalid upload reference")

                        if upload.user_id != student.id:
                            raise PermissionDenied("Upload does not belong to student")

                        # Store internal storage_path
                        value_to_store = upload.storage_path

                    else:
                        # Normal text fields
                        value_to_store = raw_value

                    answer = ApplicationAnswer(
                        application_id=application.id,
                        field_id=field.id,
                        value=value_to_store,
                    )

                    db.add(answer)


            db.commit()
            db.refresh(application)

        except Exception:
            db.rollback()
            raise

        # ---- Email after commit ----
        self.email_adapter.send_email(
            to_email=student.email,
            subject="Application Submitted",
            body=f"You have successfully applied to {internship.title}.",
        )

        self.email_adapter.send_email(
            to_email=internship.employer.email,
            subject="New Application Received",
            body=f"A new application has been submitted for '{internship.title}'.",
        )

        return application

    # ===============================
    # LIST STUDENT APPLICATIONS
    # ===============================

    def list_student_applications(self, db: Session, student):
        if student.role != "student":
            raise PermissionDenied("Not allowed")

        applications = self.repo.list_by_student(db, student.id)
        self._attach_signed_urls(applications)
        return applications


    # ===============================
    # LIST APPLICATIONS FOR INTERNSHIP (EMPLOYER)
    # ===============================

    def list_internship_applications(
        self,
        db: Session,
        employer,
        internship_id: int,
    ):
        internship = self.internship_repo.get_by_id(db, internship_id)
        if not internship:
            raise NotFoundError("Internship not found")

        if internship.employer_id != employer.id:
            raise PermissionDenied("Not allowed")

        applications = self.repo.list_by_internship(db, internship_id)
        self._attach_signed_urls(applications)
        return applications


    # ===============================
    # UPDATE APPLICATION STATUS (EMPLOYER)
    # ===============================

    def update_application_status(
        self,
        db: Session,
        employer,
        application_id: int,
        payload,
    ):
        application = self.repo.get_by_id(db, application_id)
        if not application:
            raise NotFoundError("Application not found")

        internship = self.internship_repo.get_by_id(
            db,
            application.internship_id,
        )

        if internship.employer_id != employer.id:
            raise PermissionDenied("Not allowed")

        validate_application_status_transition(
            application.status,
            payload.status,
        )

        try:
            updated = self.repo.update_status(
                db=db,
                application=application,
                new_status=payload.status,
            )

            db.commit()
            db.refresh(updated)

        except Exception:
            db.rollback()
            raise

        # Email after commit
        self.email_adapter.send_email(
            to_email=application.user.email,
            subject="Application Status Updated",
            body=f"Your application status is now {updated.status}.",
        )

        return updated

    # ===============================
    # WITHDRAW APPLICATION (STUDENT)
    # ===============================

    def withdraw_application(
        self,
        db: Session,
        student,
        application_id: int,
    ):
        if student.role != "student":
            raise PermissionDenied("Only students can withdraw applications")

        application = self.repo.get_by_id(db, application_id)
        if not application:
            raise NotFoundError("Application not found")

        if application.user_id != student.id:
            raise PermissionDenied("Not allowed")

        validate_application_status_transition(
            application.status,
            "withdrawn",
        )

        internship = self.internship_repo.get_by_id(
            db,
            application.internship_id,
        )

        try:
            updated = self.repo.update_status(
                db=db,
                application=application,
                new_status="withdrawn",
            )

            db.commit()
            db.refresh(updated)

        except Exception:
            db.rollback()
            raise

        # Email after commit
        self.email_adapter.send_email(
            to_email=internship.employer.email,
            subject="Application Withdrawn",
            body="A student has withdrawn their application.",
        )

        return updated

    def _attach_signed_urls(self, applications):
        """
        Convert stored file storage_path into signed URL dynamically.
        """

        for application in applications:
            for answer in application.answers:
                if answer.field.field_type == "file" and answer.value:
                    answer.value = self.storage_adapter.generate_signed_url(
                        answer.value
                    )
