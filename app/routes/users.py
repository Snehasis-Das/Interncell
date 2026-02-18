from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.schemas.user import UserResponse
from app.services.user_service import UserService

router = APIRouter()

user_service = UserService()


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_my_profile(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return user_service.get_user_profile(db=db, user_id=current_user.id)
