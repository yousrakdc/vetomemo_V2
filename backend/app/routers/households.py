import uuid

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user, require_role
from app.models.user import User
from app.models.membership import Membership
from app.models.enums import Role
from app.schemas.household import HouseholdMembership
from app.services import membership_service

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
    
class MemberOut(BaseModel):
    membership_id: uuid.UUID
    user_email: str
    user_name: str
    role: Role


class AddMemberRequest(BaseModel):
    email: EmailStr
    role: Role


@router.get("/{household_id}/members", response_model=list[MemberOut])
def list_members(
    household_id: uuid.UUID,
    db: Session = Depends(get_db),
    _m=Depends(require_role(Role.owner, Role.member, Role.vet_readonly)),
):
    members = membership_service.list_members(db, household_id)
    return [
        MemberOut(
            membership_id=m.id,
            user_email=m.user.email,
            user_name=m.user.full_name,
            role=m.role,
        )
        for m in members
    ]


@router.post("/{household_id}/members", response_model=MemberOut, status_code=status.HTTP_201_CREATED)
def add_member(
    household_id: uuid.UUID,
    data: AddMemberRequest,
    db: Session = Depends(get_db),
    _m=Depends(require_role(Role.owner)),  # seul le propriétaire invite
):
    membership = membership_service.add_member_by_email(
        db, household_id, data.email, data.role
    )
    return MemberOut(
        membership_id=membership.id,
        user_email=membership.user.email,
        user_name=membership.user.full_name,
        role=membership.role,
    )


@router.delete("/{household_id}/members/{membership_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_member(
    household_id: uuid.UUID,
    membership_id: uuid.UUID,
    db: Session = Depends(get_db),
    _m=Depends(require_role(Role.owner)),  # seul le propriétaire retire
):
    membership_service.remove_member(db, household_id, membership_id)