import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User
from app.models.membership import Membership
from app.models.enums import Role

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Identifiants invalides.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    subject = decode_access_token(token)
    if subject is None:
        raise credentials_exc
    try:
        user_id = uuid.UUID(subject)
    except ValueError:
        raise credentials_exc
    user = db.get(User, user_id)
    if user is None:
        raise credentials_exc
    return user


def require_role(*allowed_roles: Role):
    """Vérifie que l'utilisateur a un des rôles autorisés dans le foyer ciblé.
    Le household_id est attendu comme paramètre de chemin de la route."""

    def checker(
        household_id: uuid.UUID,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> Membership:
        membership = db.scalar(
            select(Membership).where(
                Membership.user_id == current_user.id,
                Membership.household_id == household_id,
            )
        )
        if membership is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Vous n'appartenez pas à ce foyer.",
            )
        if membership.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Rôle insuffisant pour cette action.",
            )
        return membership

    return checker