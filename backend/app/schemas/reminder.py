import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import HealthRecordType


class ReminderCreate(BaseModel):
    care_type: HealthRecordType
    title: str = Field(min_length=1, max_length=255)
    due_date: date


class ReminderUpdate(BaseModel):
    is_done: bool | None = None
    due_date: date | None = None


class ReminderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    animal_id: uuid.UUID
    care_type: HealthRecordType
    title: str
    due_date: date
    is_done: bool
    created_at: datetime