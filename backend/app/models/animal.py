import uuid
from datetime import date, datetime

from sqlalchemy import String, Date, DateTime, ForeignKey, Enum as SAEnum, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import Species


class Animal(Base):
    __tablename__ = "animals"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    household_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("households.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    species: Mapped[Species] = mapped_column(SAEnum(Species), nullable=False)
    breed: Mapped[str | None] = mapped_column(String(255), nullable=True)
    birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    household: Mapped["Household"] = relationship(back_populates="animals")
    health_records: Mapped[list["HealthRecord"]] = relationship(
        back_populates="animal", cascade="all, delete-orphan"
    )
    weight_entries: Mapped[list["WeightEntry"]] = relationship(
        back_populates="animal", cascade="all, delete-orphan"
    )
    reminders: Mapped[list["Reminder"]] = relationship(
        back_populates="animal", cascade="all, delete-orphan"
    )