import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class WeightEntryCreate(BaseModel):
    weight_kg: float = Field(gt=0, le=200)
    recorded_at: date


class WeightEntryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    animal_id: uuid.UUID
    weight_kg: float
    recorded_at: date
    created_at: datetime