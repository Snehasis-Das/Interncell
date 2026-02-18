from sqlalchemy.orm import Session
from app.repositories.internship_repository import InternshipRepository
from app.core.exceptions import PermissionDenied, NotFoundError


class InternshipService:

    def __init__(self):
        self.repo = InternshipRepository()

    def create_internship(self, db: Session, employer, payload):
        if employer.role != "employer":
            raise PermissionDenied("Only employers can create internships")

        try:
            internship = self.repo.create(
                db=db,
                employer_id=employer.id,
                payload=payload,
            )

            db.commit()
            db.refresh(internship)

            return internship

        except Exception:
            db.rollback()
            raise

    def list_internships(self, db: Session, page: int, limit: int):
        return self.repo.list(db=db, page=page, limit=limit)

    def get_internship_detail(self, db: Session, internship_id: int):
        internship = self.repo.get_by_id(db, internship_id)
        if not internship:
            raise NotFoundError("Internship not found")

        return internship

    def update_internship(self, db: Session, employer, internship_id: int, payload):
        internship = self.repo.get_by_id(db, internship_id)
        if not internship:
            raise NotFoundError("Internship not found")

        if internship.employer_id != employer.id:
            raise PermissionDenied("Not allowed")

        try:
            updated = self.repo.update(db, internship, payload)
            db.commit()
            db.refresh(updated)
            return updated

        except Exception:
            db.rollback()
            raise

    def close_internship(self, db: Session, employer, internship_id: int):
        internship = self.repo.get_by_id(db, internship_id)
        if not internship:
            raise NotFoundError("Internship not found")

        if internship.employer_id != employer.id:
            raise PermissionDenied("Not allowed")
    
        try:
            closed = self.repo.close(db, internship)
            db.commit()
            db.refresh(closed)
            return closed

        except Exception:
            db.rollback()
            raise

