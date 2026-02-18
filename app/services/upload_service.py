from sqlalchemy.orm import Session
from app.repositories.upload_repository import UploadRepository
from app.adapters.factory import get_storage_adapter
from app.core.exceptions import NotFoundError, PermissionDenied, ConflictError
from app.core.config import settings
from app.models.application_answer import ApplicationAnswer


class UploadService:

    def __init__(self):
        self.repo = UploadRepository()
        self.storage = get_storage_adapter()

    # --- QUOTA CHECK ---
    def check_quota(self, db: Session, user_id: int):
        count = self.repo.count_by_user(db, user_id)
        if count >= settings.MAX_UPLOADS_PER_USER:
            raise ConflictError("Upload quota exceeded")

    # --- RECORD UPLOAD ---
    def record_upload(
        self,
        db: Session,
        user_id: int,
        storage_path: str,
        file_name: str,
        content_type: str,
        size: int,
    ):
        return self.repo.create(
            db=db,
            user_id=user_id,
            storage_path=storage_path,
            file_name=file_name,
            content_type=content_type,
            size=size,
        )

    # --- GET SIGNED URL ---
    def generate_download_url(self, db: Session, user, upload_id: int):
        upload = self.repo.get_by_id(db, upload_id)

        if not upload:
            raise NotFoundError("Upload not found")

        if upload.user_id != user.id:
            raise PermissionDenied("Not allowed")

        signed_url = self.storage.generate_signed_url(upload.storage_path)

        return {
            "url": signed_url,
            "file_name": upload.file_name,
            "content_type": upload.content_type,
            "size": upload.size,
        }

    # --- DELETE FILE ---
    def delete_upload(self, db: Session, user, upload_id: int):
        upload = self.repo.get_by_id(db, upload_id)

        if not upload:
            raise NotFoundError("Upload not found")

        if upload.user_id != user.id:
            raise PermissionDenied("Not allowed")
        
        # Check if upload is used in any application
        is_used = (
            db.query(ApplicationAnswer)
            .filter(ApplicationAnswer.value == upload.storage_path)
            .first()
        )

        if is_used:
            raise ConflictError("Cannot delete upload used in an application")

        # delete from storage
        self.storage.delete_file(upload.storage_path)

        # delete DB record
        self.repo.delete(db, upload)

        return {"message": "Upload deleted"}
