from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.membership import Membership
from app.schemas.household import HouseholdMembership

router = APIRouter(prefix="/households", tags=["households"])


@router.get("/mine", response_model=list[HouseholdMembership])
def list_my_households(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    memberships = db.scalars(
        select(Membership).where(Membership.user_id == current_user.id)
    )
    return [
        HouseholdMembership(household=m.household, role=m.role) for m in memberships
    ]