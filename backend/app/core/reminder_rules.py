"""Règles de récurrence des soins préventifs.

Centralise toute la logique de calcul des échéances. Les règles sont
exprimées en mois d'intervalle, en fonction de l'espèce et du type de soin.
Externaliser ces règles en base de données est une évolution possible.
"""
from dataclasses import dataclass
from datetime import date

from dateutil.relativedelta import relativedelta

from app.models.enums import Species, HealthRecordType


@dataclass(frozen=True)
class RecurrenceRule:
    label: str
    interval_months: int


# (espèce, type de soin) -> règle de récurrence
RECURRENCE_RULES: dict[tuple[Species, HealthRecordType], RecurrenceRule] = {
    (Species.dog, HealthRecordType.vaccination): RecurrenceRule("Rappel vaccin annuel", 12),
    (Species.cat, HealthRecordType.vaccination): RecurrenceRule("Rappel vaccin annuel", 12),
    (Species.dog, HealthRecordType.treatment): RecurrenceRule("Antiparasitaire trimestriel", 3),
    (Species.cat, HealthRecordType.treatment): RecurrenceRule("Antiparasitaire trimestriel", 3),
    (Species.dog, HealthRecordType.visit): RecurrenceRule("Visite de contrôle annuelle", 12),
    (Species.cat, HealthRecordType.visit): RecurrenceRule("Visite de contrôle annuelle", 12),
}

# Valeur par défaut pour les espèces "other"
DEFAULT_RULE = RecurrenceRule("Contrôle annuel", 12)


def get_rule(species: Species, care_type: HealthRecordType) -> RecurrenceRule:
    return RECURRENCE_RULES.get((species, care_type), DEFAULT_RULE)


def compute_next_due_date(
    species: Species, care_type: HealthRecordType, last_date: date
) -> date:
    """Fonction pure : calcule la prochaine échéance à partir d'une date de soin.
    Aucun accès base de données — entièrement testable unitairement."""
    rule = get_rule(species, care_type)
    return last_date + relativedelta(months=rule.interval_months)