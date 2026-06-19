import uuid

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_role
from app.models.enums import Role
from app.services import weight_service, animal_service, analysis_service
from app.services.analysis_service import WeightPoint

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
