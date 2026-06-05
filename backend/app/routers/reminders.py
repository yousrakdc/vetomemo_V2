import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_role
from app.models.enums import Role
from app.schemas.reminder import ReminderCreate, ReminderUpdate, ReminderOut
from app.services import reminder_service, animal_service

router = APIRouter(
    prefix="/households/{household_id}/animals/{animal_id}/reminders",
    tags=["reminders"],
)

CAN_READ = (Role.owner, Role.member, Role.vet_readonly)
CAN_WRITE = (Role.owner, Role.member)


@router.get("", response_model=list[ReminderOut])
def list_reminders(
    household_id: uuid.UUID,
    animal_id: uuid.UUID,
    db: Session = Depends(get_db),
    _m=Depends(require_role(*CAN_READ)),
):
    animal_service.get_animal_or_404(db, household_id, animal_id)
    return reminder_service.list_reminders(db, animal_id)


@router.post("", response_model=ReminderOut, status_code=status.HTTP_201_CREATED)
def create_reminder(
    household_id: uuid.UUID,
    animal_id: uuid.UUID,
    data: ReminderCreate,
    db: Session = Depends(get_db),
    _m=Depends(require_role(*CAN_WRITE)),
):
    animal_service.get_animal_or_404(db, household_id, animal_id)
    return reminder_service.create_reminder(db, animal_id, data)


@router.patch("/{reminder_id}", response_model=ReminderOut)
def update_reminder(
    household_id: uuid.UUID,
    animal_id: uuid.UUID,
    reminder_id: uuid.UUID,
    data: ReminderUpdate,
    db: Session = Depends(get_db),
    _m=Depends(require_role(*CAN_WRITE)),
):
    animal_service.get_animal_or_404(db, household_id, animal_id)
    reminder = reminder_service.get_reminder_or_404(db, animal_id, reminder_id)
    return reminder_service.update_reminder(db, reminder, data)


@router.delete("/{reminder_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reminder(
    household_id: uuid.UUID,
    animal_id: uuid.UUID,
    reminder_id: uuid.UUID,
    db: Session = Depends(get_db),
    _m=Depends(require_role(*CAN_WRITE)),
):
    animal_service.get_animal_or_404(db, household_id, animal_id)
    reminder = reminder_service.get_reminder_or_404(db, animal_id, reminder_id)
    reminder_service.delete_reminder(db, reminder)