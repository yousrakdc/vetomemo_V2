import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import Species


class AnimalCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    species: Species
    breed: str | None = Field(default=None, max_length=255)
    birth_date: date | None = None


class AnimalUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    species: Species | None = None
    breed: str | None = Field(default=None, max_length=255)
    birth_date: date | None = None


class AnimalOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    household_id: uuid.UUID
    name: str
    species: Species
    breed: str | None
    birth_date: date | None
    created_at: datetime