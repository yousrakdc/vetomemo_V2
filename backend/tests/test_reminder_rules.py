from datetime import date

from app.core.reminder_rules import compute_next_due_date, get_rule, DEFAULT_RULE
from app.models.enums import Species, HealthRecordType


def test_vaccination_chien_un_an_plus_tard():
    """Un vaccin pour un chien doit générer une échéance un an après."""
    result = compute_next_due_date(Species.dog, HealthRecordType.vaccination, date(2026, 6, 5))
    assert result == date(2027, 6, 5)


def test_traitement_chat_trois_mois_plus_tard():
    """Un traitement antiparasitaire pour un chat : échéance à 3 mois."""
    result = compute_next_due_date(Species.cat, HealthRecordType.treatment, date(2026, 1, 15))
    assert result == date(2026, 4, 15)


def test_espece_other_utilise_regle_par_defaut():
    """Une espèce non répertoriée tombe sur la règle par défaut (12 mois)."""
    rule = get_rule(Species.other, HealthRecordType.visit)
    assert rule == DEFAULT_RULE


def test_gestion_annee_bissextile():
    """Le calcul gère correctement le passage d'une année (29 février)."""
    # 12 mois après le 29/02/2024 (bissextile) -> 28/02/2025
    result = compute_next_due_date(Species.dog, HealthRecordType.vaccination, date(2024, 2, 29))
    assert result == date(2025, 2, 28)