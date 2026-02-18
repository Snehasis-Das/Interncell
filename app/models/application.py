from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    internship_id = Column(
        Integer,
        ForeignKey("internships.id", ondelete="CASCADE"),
        nullable=False,
    )

    status = Column(String(50), default="applied", nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "internship_id", name="unique_application"),
    )

    user = relationship("User", backref="applications")
    internship = relationship("Internship", backref="applications")
    
    answers = relationship(
        "ApplicationAnswer",
        back_populates="application",
        cascade="all, delete-orphan"
    )

