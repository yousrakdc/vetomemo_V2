import uuid
from datetime import date as date_type, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import HealthRecordType


class HealthRecordCreate(BaseModel):
    type: HealthRecordType
    title: str = Field(min_length=1, max_length=255)
    date: date_type
    vet_name: str | None = Field(default=None, max_length=255)
    notes: str | None = None
    details: dict | None = None
    create_reminder: bool = True


class HealthRecordUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    date: date_type | None = None
    vet_name: str | None = Field(default=None, max_length=255)
    notes: str | None = None
    details: dict | None = None


class HealthRecordOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    animal_id: uuid.UUID
    type: HealthRecordType
    title: str
    date: date_type
    vet_name: str | None
    notes: str | None
    details: dict | None
    created_at: datetime