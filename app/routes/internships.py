from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.schemas.internship import (
    InternshipCreate,
    InternshipUpdate,
    InternshipResponse,
)
from app.services.internship_service import InternshipService
from app.schemas.application import ApplicationResponse,ApplicationCreate
from app.services.application_service import ApplicationService
from app.schemas.internship_form_field import (
    FormFieldBulkCreate,
    FormFieldResponse,
)
from app.services.internship_form_service import InternshipFormService
from app.core.rate_limiter import limiter
from fastapi import Request


router = APIRouter()

internship_service = InternshipService()
application_service = ApplicationService()
form_service = InternshipFormService()


@router.post(
    "/",
    response_model=InternshipResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_internship(
    payload: InternshipCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return internship_service.create_internship(
        db=db,
        employer=current_user,
        payload=payload,
    )


@router.get(
    "/",
    response_model=list[InternshipResponse],
)
def list_internships(
    db: Session = Depends(get_db),
    page: int = 1,
    limit: int = 20,
):
    return internship_service.list_internships(
        db=db,
        page=page,
        limit=limit,
    )


@router.get(
    "/{internship_id}",
    response_model=InternshipResponse,
)
def get_internship_detail(
    internship_id: int,
    db: Session = Depends(get_db),
):
    return internship_service.get_internship_detail(
        db=db,
        internship_id=internship_id,
    )

'''
@router.patch(
    "/{internship_id}",
    response_model=InternshipResponse,
)
def update_internship(
    internship_id: int,
    payload: InternshipUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return internship_service.update_internship(
        db=db,
        employer=current_user,
        internship_id=internship_id,
        payload=payload,
    )
'''

@router.patch(
    "/{internship_id}/close",
    response_model=InternshipResponse,
)
def close_internship(
    internship_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return internship_service.close_internship(
        db=db,
        employer=current_user,
        internship_id=internship_id,
    )

@router.post(
    "/{internship_id}/apply",
    response_model=ApplicationResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("20/minute")
def apply_to_internship(
    request: Request,
    internship_id: int,
    payload: ApplicationCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return application_service.apply_to_internship(
        db=db,
        student=current_user,
        internship_id=internship_id,
        payload=payload,
    )

@router.get(
    "/{internship_id}/applications",
    response_model=list[ApplicationResponse],
)
def list_applications_for_internship(
    internship_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return application_service.list_internship_applications(
        db=db,
        employer=current_user,
        internship_id=internship_id,
    )

@router.post(
    "/{internship_id}/form-fields",
    response_model=list[FormFieldResponse],
)
def create_form_field(
    internship_id: int,
    payload: FormFieldBulkCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return form_service.create_form_fields(
        db=db,
        employer=current_user,
        internship_id=internship_id,
        payload=payload,
    )


@router.get(
    "/{internship_id}/form-fields",
    response_model=list[FormFieldResponse],
)
def list_form_fields(
    internship_id: int,
    db: Session = Depends(get_db),
):
    return form_service.list_form_fields(
        db=db,
        internship_id=internship_id,
    )
