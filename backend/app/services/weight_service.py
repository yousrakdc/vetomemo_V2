import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.weight_entry import WeightEntry
from app.schemas.weight_entry import WeightEntryCreate


def list_weights(db: Session, animal_id: uuid.UUID) -> list[WeightEntry]:
    return list(
        db.scalars(
            select(WeightEntry)
            .where(WeightEntry.animal_id == animal_id)
            .order_by(WeightEntry.recorded_at)
        )
    )


def create_weight(db: Session, animal_id: uuid.UUID, data: WeightEntryCreate) -> WeightEntry:
    entry = WeightEntry(animal_id=animal_id, **data.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry