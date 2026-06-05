import { api } from "./api";
import { WeightEntry } from "./types";

export interface WeightInput {
  weight_kg: number;
  recorded_at: string;
}

const base = (h: string, a: string) =>
  `/households/${h}/animals/${a}/weights`;

export function listWeights(h: string, a: string) {
  return api.get<WeightEntry[]>(base(h, a));
}

export function createWeight(h: string, a: string, data: WeightInput) {
  return api.post<WeightEntry>(base(h, a), data);
}