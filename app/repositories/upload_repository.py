from sqlalchemy.orm import Session
from app.models.upload import Upload


class UploadRepository:

    def create(
        self,
        db: Session,
        user_id: int,
        storage_path: str,
        file_name: str,
        content_type: str,
        size: int,
    ):
        upload = Upload(
            user_id=user_id,
            storage_path=storage_path,
            file_name=file_name,
            content_type=content_type,
            size=size,
        )
        
        db.add(upload)
        db.commit()
        db.refresh(upload)
        
        return upload

    def count_by_user(self, db: Session, user_id: int):
        return (
            db.query(Upload)
            .filter(Upload.user_id == user_id)
            .count()
        )

    def get_by_id(self, db: Session, upload_id: int):
        return (
            db.query(Upload)
            .filter(Upload.id == upload_id)
            .first()
        )

    def list_by_user(self, db: Session, user_id: int):
        return (
            db.query(Upload)
            .filter(Upload.user_id == user_id)
            .all()
        )

    def delete(self, db: Session, upload: Upload):
        db.delete(upload)
        db.commit()