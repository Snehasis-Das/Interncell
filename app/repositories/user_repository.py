from sqlalchemy.orm import Session
from app.models.user import User


class UserRepository:

    def get_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    def get_by_id(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    def create_user(self, db: Session, email: str, password_hash: str, role: str):
        user = User(
            email=email,
            password_hash=password_hash,
            role=role,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
