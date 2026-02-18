from sqlalchemy.orm import Session
from app.models.application import Application


class ApplicationRepository:

    def get_by_id(self, db: Session, application_id: int):
        return db.query(Application).filter(
            Application.id == application_id
        ).first()

    def get_by_user_and_internship(
        self,
        db: Session,
        user_id: int,
        internship_id: int,
    ):
        return (
            db.query(Application)
            .filter(
                Application.user_id == user_id,
                Application.internship_id == internship_id,
            )
            .first()
        )

    def create(self, db: Session, user_id: int, internship_id: int):
        application = Application(
            user_id=user_id,
            internship_id=internship_id,
        )
        db.add(application)
        return application

    def list_by_student(self, db: Session, user_id: int):
        return db.query(Application).filter(
            Application.user_id == user_id
        ).all()

    def list_by_internship(self, db: Session, internship_id: int):
        return db.query(Application).filter(
            Application.internship_id == internship_id
        ).all()

    def update_status(self, db: Session, application: Application, new_status: str):
        application.status = new_status
        return application
