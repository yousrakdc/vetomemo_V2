import uuid

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.animal import Animal
from app.schemas.animal import AnimalCreate, AnimalUpdate


def list_animals(db: Session, household_id: uuid.UUID) -> list[Animal]:
    return list(
        db.scalars(
            select(Animal).where(Animal.household_id == household_id).order_by(Animal.name)
        )
    )


def get_animal_or_404(
    db: Session, household_id: uuid.UUID, animal_id: uuid.UUID
) -> Animal:
    animal = db.scalar(
        select(Animal).where(
            Animal.id == animal_id,
            Animal.household_id == household_id,
        )
    )
    if animal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Animal introuvable dans ce foyer.",
        )
    return animal


def create_animal(
    db: Session, household_id: uuid.UUID, data: AnimalCreate
) -> Animal:
    animal = Animal(household_id=household_id, **data.model_dump())
    db.add(animal)
    db.commit()
    db.refresh(animal)
    return animal


def update_animal(
    db: Session, animal: Animal, data: AnimalUpdate
) -> Animal:
    updates = data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(animal, field, value)
    db.commit()
    db.refresh(animal)
    return animal


def delete_animal(db: Session, animal: Animal) -> None:
    db.delete(animal)
    db.commit()