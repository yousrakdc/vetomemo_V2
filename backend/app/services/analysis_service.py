"""Analyse des courbes de poids : détection d'anomalies et projection de tendance.

Fonctions pures (aucun accès base de données) pour rester testables unitairement.
Méthodes volontairement simples et explicables :
- anomalies par z-score sur l'historique de l'animal
- tendance par régression linéaire (moindres carrés)
"""
from dataclasses import dataclass
from datetime import date, timedelta

import numpy as np


# En dessous de ce nombre de pesées, on ne tire aucune conclusion statistique.
MIN_POINTS_FOR_ANOMALY = 4
# Seuil de z-score au-delà duquel une pesée est considérée comme anormale.
ZSCORE_THRESHOLD = 2.0
# Nombre de pesées minimal pour calculer une tendance.
MIN_POINTS_FOR_TREND = 3


@dataclass
class WeightPoint:
    id: str
    recorded_at: date
    weight_kg: float


@dataclass
class AnomalyResult:
    anomaly_ids: list[str]
    mean: float | None
    std: float | None
    threshold: float
    enough_data: bool


@dataclass
class TrendResult:
    enough_data: bool
    slope_kg_per_day: float | None
    projected_weight_30d: float | None
    direction: str  # "hausse", "baisse", "stable", ou "indéterminé"


def detect_anomalies(points: list[WeightPoint]) -> AnomalyResult:
    """Signale les pesées dont le z-score dépasse le seuil.
    z = (valeur - moyenne) / écart-type."""
    if len(points) < MIN_POINTS_FOR_ANOMALY:
        return AnomalyResult([], None, None, ZSCORE_THRESHOLD, enough_data=False)

    weights = np.array([p.weight_kg for p in points], dtype=float)
    mean = float(weights.mean())
    std = float(weights.std(ddof=0))

    # Si tous les poids sont identiques, std=0 : aucune anomalie possible.
    if std == 0:
        return AnomalyResult([], mean, std, ZSCORE_THRESHOLD, enough_data=True)

    zscores = np.abs((weights - mean) / std)
    anomaly_ids = [
        points[i].id for i in range(len(points)) if zscores[i] > ZSCORE_THRESHOLD
    ]
    return AnomalyResult(anomaly_ids, mean, std, ZSCORE_THRESHOLD, enough_data=True)


def compute_trend(points: list[WeightPoint]) -> TrendResult:
    """Régression linéaire des poids dans le temps (moindres carrés).
    Renvoie la pente en kg/jour et une projection à 30 jours."""
    if len(points) < MIN_POINTS_FOR_TREND:
        return TrendResult(False, None, None, "indéterminé")

    # On ordonne par date et on convertit les dates en nombre de jours écoulés.
    ordered = sorted(points, key=lambda p: p.recorded_at)
    t0 = ordered[0].recorded_at
    xs = np.array([(p.recorded_at - t0).days for p in ordered], dtype=float)
    ys = np.array([p.weight_kg for p in ordered], dtype=float)

    # np.polyfit degré 1 = régression linéaire : renvoie [pente, ordonnée]
    slope, intercept = np.polyfit(xs, ys, 1)

    last_day = xs[-1]
    projected = float(slope * (last_day + 30) + intercept)

    # Seuil de significativité de la pente (kg/jour) pour éviter le bruit.
    if abs(slope) < 0.005:
        direction = "stable"
    elif slope > 0:
        direction = "hausse"
    else:
        direction = "baisse"

    return TrendResult(
        enough_data=True,
        slope_kg_per_day=float(slope),
        projected_weight_30d=round(projected, 2),
        direction=direction,
    )
