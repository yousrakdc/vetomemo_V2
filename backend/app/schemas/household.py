import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import Role


class HouseholdOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    created_at: datetime


class HouseholdMembership(BaseModel):
    """Un foyer avec le rôle de l'utilisateur courant dedans."""
    model_config = ConfigDict(from_attributes=True)

    household: HouseholdOut
    role: Role