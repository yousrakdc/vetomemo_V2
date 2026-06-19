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

export function analyzeWeight(householdId: string, animalId: string) {
  return api.get<WeightAnalysis>(
    `/households/${householdId}/animals/${animalId}/analysis/weight`
  );
}