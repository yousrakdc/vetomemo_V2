"""Assignation d'un animal à un profil de référence issu du clustering.

Les profils de référence sont les centres des clusters découverts dans le
notebook d'exploration (k-means, k=4, sur le dataset chats). L'apprentissage
est fait offline (notebook) ; ici on fait uniquement de l'inférence :
on assigne un animal au profil de référence le plus proche (distance euclidienne
sur l'âge et le poids).
"""
from dataclasses import dataclass
from datetime import date

import numpy as np

from app.models.enums import Species


@dataclass
class Profile:
    key: str
    label: str
    center_age: float       # âge moyen du profil (années)
    center_weight: float    # poids moyen du profil (kg)
    suggested_care: list[str]


# Profils de référence issus du notebook (centres des 4 clusters de chats).
CAT_PROFILES: list[Profile] = [
    Profile(
        key="young_light",
        label="Jeune et de petit gabarit",
        center_age=5.4,
        center_weight=3.6,
        suggested_care=[
            "Vaccinations de rappel à jour",
            "Bilan dentaire annuel",
            "Surveillance du poids une fois par an",
        ],
    ),
    Profile(
        key="young_heavy",
        label="Jeune et de fort gabarit",
        center_age=5.4,
        center_weight=7.5,
        suggested_care=[
            "Suivi du poids renforcé (risque de surpoids)",
            "Conseil nutritionnel adapté au gabarit",
            "Encouragement à l'activité physique",
        ],
    ),
    Profile(
        key="senior_light",
        label="Senior et de petit gabarit",
        center_age=15.0,
        center_weight=3.6,
        suggested_care=[
            "Bilan gériatrique annuel (reins, thyroïde)",
            "Surveillance de la perte de poids",
            "Contrôle dentaire rapproché",
        ],
    ),
    Profile(
        key="senior_heavy",
        label="Senior et de fort gabarit",
        center_age=15.1,
        center_weight=7.5,
        suggested_care=[
            "Bilan gériatrique annuel",
            "Suivi articulaire (poids + âge)",
            "Surveillance cardiaque et du poids",
        ],
    ),
]


def compute_age_years(birth_date: date | None, today: date | None = None) -> float | None:
    if birth_date is None:
        return None
    today = today or date.today()
    days = (today - birth_date).days
    return round(days / 365.25, 1)


def assign_profile(species: Species, age_years: float | None, weight_kg: float | None) -> Profile | None:
    """Assigne l'animal au profil de référence le plus proche.
    Renvoie None si l'espèce n'est pas couverte ou si les données manquent."""
    if species != Species.cat:
        return None
    if age_years is None or weight_kg is None:
        return None

    point = np.array([age_years, weight_kg], dtype=float)
    best_profile = None
    best_distance = None
    for profile in CAT_PROFILES:
        center = np.array([profile.center_age, profile.center_weight], dtype=float)
        distance = float(np.linalg.norm(point - center))
        if best_distance is None or distance < best_distance:
            best_distance = distance
            best_profile = profile
    return best_profile
