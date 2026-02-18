from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class ApplicationAnswer(Base):
    __tablename__ = "application_answers"

    id = Column(Integer, primary_key=True, index=True)

    application_id = Column(
        Integer,
        ForeignKey("applications.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    field_id = Column(
        Integer,
        ForeignKey("internship_form_fields.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    value = Column(Text, nullable=False)

    application = relationship("Application", back_populates="answers")
    field = relationship("InternshipFormField")
    
    @property
    def field_key(self):
        return self.field.field_key


    @property
    def label(self):
        return self.field.label
