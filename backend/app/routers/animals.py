import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_role
from app.models.enums import Role
from app.schemas.animal import AnimalCreate, AnimalUpdate, AnimalOut
from app.services import animal_service

router = APIRouter(prefix="/households/{household_id}/animals", tags=["animals"])

# Rôles autorisés à lire / à modifier
CAN_READ = (Role.owner, Role.member, Role.vet_readonly)
CAN_WRITE = (Role.owner, Role.member)


@router.get("", response_model=list[AnimalOut])
def list_animals(
    household_id: uuid.UUID,
    db: Session = Depends(get_db),
    _membership=Depends(require_role(*CAN_READ)),
):
    return animal_service.list_animals(db, household_id)


@router.post("", response_model=AnimalOut, status_code=status.HTTP_201_CREATED)
def create_animal(
    household_id: uuid.UUID,
    data: AnimalCreate,
    db: Session = Depends(get_db),
    _membership=Depends(require_role(*CAN_WRITE)),
):
    return animal_service.create_animal(db, household_id, data)


@router.get("/{animal_id}", response_model=AnimalOut)
def get_animal(
    household_id: uuid.UUID,
    animal_id: uuid.UUID,
    db: Session = Depends(get_db),
    _membership=Depends(require_role(*CAN_READ)),
):
    return animal_service.get_animal_or_404(db, household_id, animal_id)


@router.patch("/{animal_id}", response_model=AnimalOut)
def update_animal(
    household_id: uuid.UUID,
    animal_id: uuid.UUID,
    data: AnimalUpdate,
    db: Session = Depends(get_db),
    _membership=Depends(require_role(*CAN_WRITE)),
):
    animal = animal_service.get_animal_or_404(db, household_id, animal_id)
    return animal_service.update_animal(db, animal, data)


@router.delete("/{animal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_animal(
    household_id: uuid.UUID,
    animal_id: uuid.UUID,
    db: Session = Depends(get_db),
    _membership=Depends(require_role(Role.owner)),
):
    animal = animal_service.get_animal_or_404(db, household_id, animal_id)
    animal_service.delete_animal(db, animal)