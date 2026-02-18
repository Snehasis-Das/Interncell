from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import UserRegister, UserLogin, TokenResponse
from app.services.auth_service import AuthService
from app.core.rate_limiter import limiter
from fastapi import Request


router = APIRouter()

auth_service = AuthService()


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("5/minute")
def register_user(
    request: Request,
    payload: UserRegister,
    db: Session = Depends(get_db),
):
    return auth_service.register_user(db=db, payload=payload)


@router.post(
    "/login",
    response_model=TokenResponse,
)
@limiter.limit("5/minute")
def login_user(
    request: Request,
    payload: UserLogin,
    db: Session = Depends(get_db),
):
    return auth_service.login_user(db=db, payload=payload)
