from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import Enum
from app.enums.internship_status import (
    InternshipStatus,
    InternshipWorkMode,
    InternshipTiming,
)
from sqlalchemy import Enum as SAEnum
from app.db.base import Base


class Internship(Base):
    __tablename__ = "internships"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)

    # NEW FIELDS (nullable for safe migration)
    details = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)

    work_mode = Column(
        SAEnum(
            InternshipWorkMode,
            values_callable=lambda x: [e.value for e in x],
            name="internship_work_mode",
        ),
        nullable=True,
    )

    timing = Column(
        SAEnum(
            InternshipTiming,
            values_callable=lambda x: [e.value for e in x],
            name="internship_timing",
        ),
        nullable=True,
    )

    experience_min_years = Column(Integer, nullable=True)
    duration_weeks = Column(Integer, nullable=True)

    stipend_amount = Column(Integer, nullable=True)
    stipend_currency = Column(String(10), nullable=True)

    application_deadline = Column(DateTime(timezone=True), nullable=True)

    status = Column(
        SAEnum(
            InternshipStatus,
            values_callable=lambda x: [e.value for e in x],
            name="internship_status",
        ),
        default=InternshipStatus.OPEN,
        nullable=False,
    )

    employer_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    employer = relationship("User", backref="internships")

    form_fields = relationship(
        "InternshipFormField",
        back_populates="internship",
        cascade="all, delete-orphan",
    )
