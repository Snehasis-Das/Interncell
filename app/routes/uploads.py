from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4

from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.adapters.factory import get_storage_adapter
from app.services.upload_service import UploadService
from app.core.config import settings
from app.core.rate_limiter import limiter
from fastapi import Request


router = APIRouter()

storage = get_storage_adapter()
upload_service = UploadService()

MAX_FILE_SIZE = settings.MAX_UPLOAD_SIZE
ALLOWED_TYPES = settings.ALLOWED_UPLOAD_TYPES.split(",")


@router.post("/")
@limiter.limit("10/minute")
def upload_file(
    request: Request,
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Invalid file")

    # Validate content type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    # Validate file size
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)

    if size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")

    # Enforce upload quota
    upload_service.check_quota(db, current_user.id)

    # Generate destination key
    destination_name = f"{current_user.id}_{uuid4()}_{file.filename}"

    try:
        # 1️⃣ Upload → returns blob_name (NOT url)
        storage_path = storage.upload_file(
            file=file.file,
            destination_path=destination_name,
            content_type=file.content_type,
        )

        # 2️⃣ Save metadata in DB
        upload_record = upload_service.record_upload(
            db=db,
            user_id=current_user.id,
            storage_path=storage_path,
            file_name=file.filename,
            content_type=file.content_type,
            size=size,
        )

        # 3️⃣ Generate signed URL for response
        signed_url = storage.generate_signed_url(storage_path)

        return {
            "upload_id": upload_record.id,
            "url": signed_url,
            "filename": file.filename,
            "content_type": file.content_type,
            "size": size,
        }

    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Upload failed")

@router.get("/{upload_id}")
def download_upload(
    upload_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return upload_service.generate_download_url(
        db=db,
        user=current_user,
        upload_id=upload_id,
    )


@router.delete("/{upload_id}")
def delete_upload(
    upload_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return upload_service.delete_upload(
        db=db,
        user=current_user,
        upload_id=upload_id,
    )
