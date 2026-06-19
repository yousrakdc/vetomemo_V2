import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_role
from app.models.enums import Role
from app.schemas.weight_entry import WeightEntryCreate, WeightEntryOut
from app.services import weight_service, animal_service
from app.core.ws_manager import manager

router = APIRouter(
    prefix="/households/{household_id}/animals/{animal_id}/weights",
    tags=["weights"],
)

CAN_READ = (Role.owner, Role.member, Role.vet_readonly)
CAN_WRITE = (Role.owner, Role.member)


@router.get("", response_model=list[WeightEntryOut])
def list_weights(
    household_id: uuid.UUID,
    animal_id: uuid.UUID,
    db: Session = Depends(get_db),
    _m=Depends(require_role(*CAN_READ)),
):
    animal_service.get_animal_or_404(db, household_id, animal_id)
    return weight_service.list_weights(db, animal_id)


@router.post("", response_model=WeightEntryOut, status_code=status.HTTP_201_CREATED)
async def create_weight(
    household_id: uuid.UUID,
    animal_id: uuid.UUID,
    data: WeightEntryCreate,
    db: Session = Depends(get_db),
    _m=Depends(require_role(*CAN_WRITE)),
):
    animal = animal_service.get_animal_or_404(db, household_id, animal_id)
    entry = weight_service.create_weight(db, animal_id, data)
    await manager.publish(
        str(household_id),
        {
            "type": "weight_created",
            "animal_id": str(animal_id),
            "animal_name": animal.name,
            "weight_kg": entry.weight_kg,
        },
    )
    return entry