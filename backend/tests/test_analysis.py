from datetime import date, timedelta

from app.services.analysis_service import (
    detect_anomalies,
    compute_trend,
    WeightPoint,
    MIN_POINTS_FOR_ANOMALY,
)


def _make_points(weights: list[float]) -> list[WeightPoint]:
    """Construit une liste de pesées à des dates espacées d'un jour."""
    base = date(2026, 1, 1)
    return [
        WeightPoint(id=str(i), recorded_at=base + timedelta(days=i), weight_kg=w)
        for i, w in enumerate(weights)
    ]


def test_pas_assez_de_donnees():
    """En dessous du seuil, aucune anomalie et enough_data=False."""
    points = _make_points([10.0, 10.1])  # 2 points < seuil
    result = detect_anomalies(points)
    assert result.enough_data is False
    assert result.anomaly_ids == []


def test_detecte_valeur_aberrante():
    """Une valeur très éloignée de la moyenne est signalée."""
    # quatre poids cohérents + une aberration
    points = _make_points([10.0, 10.1, 9.9, 10.0, 10.2, 10.0, 9.8, 16.0])
    result = detect_anomalies(points)
    assert result.enough_data is True
    # le dernier point (index 7, valeur 16.0) doit être signalé
    assert "7" in result.anomaly_ids


def test_aucune_anomalie_si_poids_stables():
    """Des poids homogènes ne déclenchent aucune anomalie."""
    points = _make_points([10.0, 10.1, 9.9, 10.0, 10.05])
    result = detect_anomalies(points)
    assert result.anomaly_ids == []


def test_tendance_hausse():
    """Une série croissante donne une tendance 'hausse'."""
    points = _make_points([5.0, 5.5, 6.0, 6.5, 7.0])
    result = compute_trend(points)
    assert result.enough_data is True
    assert result.direction == "hausse"
    assert result.slope_kg_per_day > 0


def test_tendance_baisse():
    """Une série décroissante donne une tendance 'baisse'."""
    points = _make_points([8.0, 7.5, 7.0, 6.5, 6.0])
    result = compute_trend(points)
    assert result.direction == "baisse"


def test_tendance_indeterminee_si_trop_peu_de_points():
    """Moins de points que le minimum : tendance indéterminée."""
    points = _make_points([5.0, 6.0])
    result = compute_trend(points)
    assert result.enough_data is False
    assert result.direction == "indéterminé"