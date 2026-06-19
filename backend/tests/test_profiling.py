from datetime import date

from app.services.profiling_service import assign_profile, compute_age_years
from app.models.enums import Species


def test_chien_non_couvert():
    """La suggestion de profil ne concerne que les chats."""
    result = assign_profile(Species.dog, age_years=5.0, weight_kg=20.0)
    assert result is None


def test_donnees_manquantes():
    """Sans âge ou sans poids, pas de profil."""
    assert assign_profile(Species.cat, age_years=None, weight_kg=4.0) is None
    assert assign_profile(Species.cat, age_years=5.0, weight_kg=None) is None


def test_jeune_leger_assigne_bon_profil():
    """Un chat jeune et léger doit tomber sur le profil 'young_light'."""
    result = assign_profile(Species.cat, age_years=5.0, weight_kg=3.5)
    assert result is not None
    assert result.key == "young_light"


def test_senior_lourd_assigne_bon_profil():
    """Un chat âgé et lourd doit tomber sur le profil 'senior_heavy'."""
    result = assign_profile(Species.cat, age_years=15.0, weight_kg=7.5)
    assert result is not None
    assert result.key == "senior_heavy"


def test_compute_age_years():
    """Le calcul d'âge en années à partir d'une date de naissance."""
    naissance = date(2020, 1, 1)
    reference = date(2026, 1, 1)
    age = compute_age_years(naissance, today=reference)
    assert 5.9 <= age <= 6.1  # environ 6 ans


def test_compute_age_none():
    """Sans date de naissance, l'âge est None."""
    assert compute_age_years(None) is None