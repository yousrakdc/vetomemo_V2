import uuid

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_role
from app.models.enums import Role
from app.services import weight_service, animal_service, analysis_service, profiling_service
from app.services.profiling_service import compute_age_years, assign_profile

router = APIRouter(
    prefix="/households/{household_id}/animals/{animal_id}/analysis",
    tags=["analysis"],
)

CAN_READ = (Role.owner, Role.member, Role.vet_readonly)


class AnomalyOut(BaseModel):
    anomaly_ids: list[str]
    mean: float | None
    std: float | None
    threshold: float
    enough_data: bool


class TrendOut(BaseModel):
    enough_data: bool
    slope_kg_per_day: float | None
    projected_weight_30d: float | None
    direction: str


class WeightAnalysisOut(BaseModel):
    anomalies: AnomalyOut
    trend: TrendOut


@router.get("/weight", response_model=WeightAnalysisOut)
def analyze_weight(
    household_id: uuid.UUID,
    animal_id: uuid.UUID,
    db: Session = Depends(get_db),
    _m=Depends(require_role(*CAN_READ)),
):
    animal_service.get_animal_or_404(db, household_id, animal_id)
    entries = weight_service.list_weights(db, animal_id)

    points = [
        WeightPoint(id=str(e.id), recorded_at=e.recorded_at, weight_kg=e.weight_kg)
        for e in entries
    ]

    anomalies = analysis_service.detect_anomalies(points)
    trend = analysis_service.compute_trend(points)

    return WeightAnalysisOut(
        anomalies=AnomalyOut(**anomalies.__dict__),
        trend=TrendOut(**trend.__dict__),
    )

class ProfileOut(BaseModel):
    available: bool
    profile_key: str | None = None
    profile_label: str | None = None
    suggested_care: list[str] = []
    reason: str | None = None  # explication si indisponible


@router.get("/profile", response_model=ProfileOut)
def get_profile(
    household_id: uuid.UUID,
    animal_id: uuid.UUID,
    db: Session = Depends(get_db),
    _m=Depends(require_role(*CAN_READ)),
):
    animal = animal_service.get_animal_or_404(db, household_id, animal_id)

    # On a besoin de l'âge (depuis birth_date) et du dernier poids connu.
    age_years = compute_age_years(animal.birth_date)
    weights = weight_service.list_weights(db, animal_id)
    last_weight = weights[-1].weight_kg if weights else None

    profile = assign_profile(animal.species, age_years, last_weight)

    if profile is None:
        # Expliquer pourquoi, c'est plus utile qu'un simple "indisponible"
        if animal.species.value != "cat":
            reason = "La suggestion de profil n'est disponible que pour les chats pour l'instant."
        elif age_years is None:
            reason = "Renseignez la date de naissance pour activer la suggestion."
        else:
            reason = "Ajoutez au moins une pesée pour activer la suggestion."
        return ProfileOut(available=False, reason=reason)

    return ProfileOut(
        available=True,
        profile_key=profile.key,
        profile_label=profile.label,
        suggested_care=profile.suggested_care,
    )
