from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.schemas.application import (
    ApplicationResponse,
    ApplicationStatusUpdate,
)
from app.services.application_service import ApplicationService

router = APIRouter()

application_service = ApplicationService()


@router.get(
    "/me",
    response_model=list[ApplicationResponse],
)
def list_my_applications(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return application_service.list_student_applications(
        db=db,
        student=current_user,
    )

@router.patch(
    "/{application_id}",
    response_model=ApplicationResponse,
)
def update_application_status(
    application_id: int,
    payload: ApplicationStatusUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return application_service.update_application_status(
        db=db,
        employer=current_user,
        application_id=application_id,
        payload=payload,
    )

@router.patch(
    "/{application_id}/withdraw",
    response_model=ApplicationResponse,
)
def withdraw_application(
    application_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return application_service.withdraw_application(
        db=db,
        student=current_user,
        application_id=application_id,
    )
