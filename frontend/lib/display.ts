import { Species, HealthRecordType } from "./types";

export const SPECIES_LABELS: Record<Species, string> = {
  dog: "Chien",
  cat: "Chat",
  other: "Autre",
};

export const SPECIES_EMOJI: Record<Species, string> = {
  dog: "🐕",
  cat: "🐈",
  other: "🐾",
};

export const CARE_LABELS: Record<HealthRecordType, string> = {
  visit: "Visite",
  vaccination: "Vaccination",
  treatment: "Traitement",
};

export const CARE_BADGE_CLASS: Record<HealthRecordType, string> = {
  visit: "badge badge-visit",
  vaccination: "badge badge-vaccination",
  treatment: "badge badge-treatment",
};