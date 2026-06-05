import uuid

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.health_record import HealthRecord
from app.models.animal import Animal
from app.schemas.health_record import HealthRecordCreate, HealthRecordUpdate
from app.services import reminder_service


def list_health_records(db: Session, animal_id: uuid.UUID) -> list[HealthRecord]:
    return list(
        db.scalars(
            select(HealthRecord)
            .where(HealthRecord.animal_id == animal_id)
            .order_by(HealthRecord.date.desc())
        )
    )


def get_record_or_404(db: Session, animal_id: uuid.UUID, record_id: uuid.UUID) -> HealthRecord:
    record = db.scalar(
        select(HealthRecord).where(
            HealthRecord.id == record_id, HealthRecord.animal_id == animal_id
        )
    )
    if record is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Soin introuvable.")
    return record


def create_health_record(
    db: Session, animal: Animal, data: HealthRecordCreate
) -> HealthRecord:
    payload = data.model_dump(exclude={"create_reminder"})
    record = HealthRecord(animal_id=animal.id, **payload)
    db.add(record)
    db.commit()
    db.refresh(record)

    # Génération automatique du rappel de suivi
    if data.create_reminder:
        reminder_service.create_auto_reminder(db, animal, data.type, data.date)

    return record


def update_health_record(
    db: Session, record: HealthRecord, data: HealthRecordUpdate
) -> HealthRecord:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(record, field, value)
    db.commit()
    db.refresh(record)
    return record


def delete_health_record(db: Session, record: HealthRecord) -> None:
    db.delete(record)
    db.commit()