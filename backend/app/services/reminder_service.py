import uuid

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.reminder import Reminder
from app.models.animal import Animal
from app.models.enums import HealthRecordType
from app.core.reminder_rules import compute_next_due_date, get_rule
from app.schemas.reminder import ReminderCreate, ReminderUpdate


def list_reminders(db: Session, animal_id: uuid.UUID) -> list[Reminder]:
    return list(
        db.scalars(
            select(Reminder)
            .where(Reminder.animal_id == animal_id)
            .order_by(Reminder.due_date)
        )
    )


def get_reminder_or_404(db: Session, animal_id: uuid.UUID, reminder_id: uuid.UUID) -> Reminder:
    reminder = db.scalar(
        select(Reminder).where(
            Reminder.id == reminder_id, Reminder.animal_id == animal_id
        )
    )
    if reminder is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Rappel introuvable.")
    return reminder


def create_reminder(db: Session, animal_id: uuid.UUID, data: ReminderCreate) -> Reminder:
    reminder = Reminder(animal_id=animal_id, **data.model_dump())
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder


def create_auto_reminder(
    db: Session, animal: Animal, care_type: HealthRecordType, from_date
) -> Reminder:
    """Génère un rappel automatique à partir d'un soin enregistré."""
    rule = get_rule(animal.species, care_type)
    due = compute_next_due_date(animal.species, care_type, from_date)
    reminder = Reminder(
        animal_id=animal.id,
        care_type=care_type,
        title=rule.label,
        due_date=due,
    )
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder


def update_reminder(db: Session, reminder: Reminder, data: ReminderUpdate) -> Reminder:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(reminder, field, value)
    db.commit()
    db.refresh(reminder)
    return reminder


def delete_reminder(db: Session, reminder: Reminder) -> None:
    db.delete(reminder)
    db.commit()