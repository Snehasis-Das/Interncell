from sqlalchemy.orm import Session
from app.schemas.auth import UserRegister, UserLogin
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password, create_access_token
from app.core.exceptions import AuthenticationError, ConflictError
from app.adapters.factory import get_email_adapter

class AuthService:

    def __init__(self):
        self.user_repo = UserRepository()
        self.email_adapter = get_email_adapter()

    def register_user(self, db: Session, payload):
        try:
            existing_user = self.user_repo.get_by_email(db, payload.email)
            if existing_user:
                raise ConflictError("Email already registered")

            hashed_password = hash_password(payload.password)

            user = self.user_repo.create_user(
                db=db,
                email=payload.email,
                password_hash=hashed_password,
                role=payload.role,
            )

            db.commit()
            db.refresh(user)

        except Exception:
            db.rollback()
            raise
        
        self.email_adapter.send_email(
                to_email=user.email,
                subject="Welcome to Interncell",
                body="Your account has been successfully created.",
            )

        return user


    def login_user(self, db: Session, payload: UserLogin):
        user = self.user_repo.get_by_email(db, payload.email)
        if not user:
            raise AuthenticationError("Invalid credentials")

        if not verify_password(payload.password, user.password_hash):
            raise AuthenticationError("Invalid credentials")

        token = create_access_token({
            "user_id": user.id,
            "role": user.role,
        })

        return {
            "access_token": token,
            "token_type": "bearer",
        }
