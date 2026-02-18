from sqlalchemy.orm import Session
from app.models.internship import Internship
from app.utils.pagination import apply_pagination


class InternshipRepository:

    def create(self, db: Session, employer_id: int, payload):
        internship = Internship(
            title=payload.title,
            description=payload.description,
            details=payload.details,
            location=payload.location,
            work_mode=payload.work_mode,
            timing=payload.timing,
            experience_min_years=payload.experience_min_years,
            duration_weeks=payload.duration_weeks,
            stipend_amount=payload.stipend_amount,
            stipend_currency=payload.stipend_currency,
            application_deadline=payload.application_deadline,
            employer_id=employer_id,
        )
        db.add(internship)
        return internship

    def get_by_id(self, db: Session, internship_id: int):
        return db.query(Internship).filter(
            Internship.id == internship_id
        ).first()

    def list(self, db: Session, page: int, limit: int):
        query = db.query(Internship)
        query = apply_pagination(query, page, limit)
        return query.all()

    def update(self, db: Session, internship: Internship, payload):
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(internship, key, value)
        return internship

    def close(self, db: Session, internship: Internship):
        internship.status = "closed"
        return internship
