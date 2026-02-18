from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.enums.form_field_type import FormFieldType
from sqlalchemy import UniqueConstraint


class InternshipFormField(Base):
    __tablename__ = "internship_form_fields"

    id = Column(Integer, primary_key=True, index=True)

    internship_id = Column(
        Integer,
        ForeignKey("internships.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    field_key = Column(String(100), nullable=False)  # employer-defined unique key
    label = Column(String(255), nullable=False)
    field_type = Column(String(50), nullable=False, default=FormFieldType.TEXT.value)
    is_required = Column(Boolean, default=False)

    internship = relationship("Internship", back_populates="form_fields")

    __table_args__ = (
        UniqueConstraint("internship_id", "field_key", name="uq_field_per_internship"),
    )
