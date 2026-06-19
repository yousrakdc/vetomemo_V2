import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_role
from app.models.enums import Role
from app.schemas.health_record import HealthRecordCreate, HealthRecordUpdate, HealthRecordOut
from app.services import health_record_service, animal_service
from app.core.ws_manager import manager

router = APIRouter(
    prefix="/households/{household_id}/animals/{animal_id}/health-records",
    tags=["health-records"],
)

CAN_READ = (Role.owner, Role.member, Role.vet_readonly)
CAN_WRITE = (Role.owner, Role.member)


@router.get("", response_model=list[HealthRecordOut])
def list_records(
    household_id: uuid.UUID,
    animal_id: uuid.UUID,
    db: Session = Depends(get_db),
    _m=Depends(require_role(*CAN_READ)),
):
    animal_service.get_animal_or_404(db, household_id, animal_id)
    return health_record_service.list_health_records(db, animal_id)


@router.post("", response_model=HealthRecordOut, status_code=status.HTTP_201_CREATED)
async def create_record(
    household_id: uuid.UUID,
    animal_id: uuid.UUID,
    data: HealthRecordCreate,
    db: Session = Depends(get_db),
    _m=Depends(require_role(*CAN_WRITE)),
):
    animal = animal_service.get_animal_or_404(db, household_id, animal_id)
    record = health_record_service.create_health_record(db, animal, data)
    await manager.publish(
        str(household_id),
        {
            "type": "health_record_created",
            "animal_id": str(animal_id),
            "animal_name": animal.name,
            "title": record.title,
        },
    )
    return record


@router.patch("/{record_id}", response_model=HealthRecordOut)
def update_record(
    household_id: uuid.UUID,
    animal_id: uuid.UUID,
    record_id: uuid.UUID,
    data: HealthRecordUpdate,
    db: Session = Depends(get_db),
    _m=Depends(require_role(*CAN_WRITE)),
):
    animal_service.get_animal_or_404(db, household_id, animal_id)
    record = health_record_service.get_record_or_404(db, animal_id, record_id)
    return health_record_service.update_health_record(db, record, data)


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_record(
    household_id: uuid.UUID,
    animal_id: uuid.UUID,
    record_id: uuid.UUID,
    db: Session = Depends(get_db),
    _m=Depends(require_role(*CAN_WRITE)),
):
    animal_service.get_animal_or_404(db, household_id, animal_id)
    record = health_record_service.get_record_or_404(db, animal_id, record_id)
    health_record_service.delete_health_record(db, record)