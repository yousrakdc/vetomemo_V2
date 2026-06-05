import { api } from "./api";
import { Animal, Species } from "./types";

export interface AnimalInput {
  name: string;
  species: Species;
  breed?: string | null;
  birth_date?: string | null;
}

export function listAnimals(householdId: string) {
  return api.get<Animal[]>(`/households/${householdId}/animals`);
}

export function createAnimal(householdId: string, data: AnimalInput) {
  return api.post<Animal>(`/households/${householdId}/animals`, data);
}

export function getAnimal(householdId: string, animalId: string) {
  return api.get<Animal>(`/households/${householdId}/animals/${animalId}`);
}

export function deleteAnimal(householdId: string, animalId: string) {
  return api.delete<void>(`/households/${householdId}/animals/${animalId}`);
}