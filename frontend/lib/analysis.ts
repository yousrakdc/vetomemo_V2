import { api } from "./api";

export interface WeightAnalysis {
  anomalies: {
    anomaly_ids: string[];
    mean: number | null;
    std: number | null;
    threshold: number;
    enough_data: boolean;
  };
  trend: {
    enough_data: boolean;
    slope_kg_per_day: number | null;
    projected_weight_30d: number | null;
    direction: string;
  };
}

export interface AnimalProfile {
  available: boolean;
  profile_key: string | null;
  profile_label: string | null;
  suggested_care: string[];
  reason: string | null;
}

export function getAnimalProfile(householdId: string, animalId: string) {
  return api.get<AnimalProfile>(
    `/households/${householdId}/animals/${animalId}/analysis/profile`
  );
}

export function analyzeWeight(householdId: string, animalId: string) {
  return api.get<WeightAnalysis>(
    `/households/${householdId}/animals/${animalId}/analysis/weight`
  );
}