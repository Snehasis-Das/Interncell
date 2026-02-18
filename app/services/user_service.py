from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.core.exceptions import NotFoundError


class UserService:

    def __init__(self):
        self.user_repo = UserRepository()

    def get_user_profile(self, db: Session, user_id: int):
        user = self.user_repo.get_by_id(db, user_id)
        if not user:
            raise NotFoundError("User not found")

        return user
