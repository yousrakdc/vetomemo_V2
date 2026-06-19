import uuid

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.membership import Membership
from app.models.enums import Role


def list_members(db: Session, household_id: uuid.UUID) -> list[Membership]:
    return list(
        db.scalars(
            select(Membership).where(Membership.household_id == household_id)
        )
    )


def add_member_by_email(
    db: Session, household_id: uuid.UUID, email: str, role: Role
) -> Membership:
    # L'utilisateur doit déjà exister
    user = db.scalar(select(User).where(User.email == email))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucun utilisateur inscrit avec cet email.",
        )

    # Pas de doublon : un utilisateur ne peut être qu'une fois dans un foyer
    existing = db.scalar(
        select(Membership).where(
            Membership.user_id == user.id,
            Membership.household_id == household_id,
        )
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cet utilisateur est déjà membre du foyer.",
        )

    # On n'attribue pas le rôle 'owner' par invitation
    if role == Role.owner:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le rôle propriétaire ne peut pas être attribué par invitation.",
        )

    membership = Membership(user_id=user.id, household_id=household_id, role=role)
    db.add(membership)
    db.commit()
    db.refresh(membership)
    return membership


def remove_member(db: Session, household_id: uuid.UUID, membership_id: uuid.UUID) -> None:
    membership = db.scalar(
        select(Membership).where(
            Membership.id == membership_id,
            Membership.household_id == household_id,
        )
    )
    if membership is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Membre introuvable.")
    if membership.role == Role.owner:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le propriétaire ne peut pas être retiré du foyer.",
        )
    db.delete(membership)
    db.commit()