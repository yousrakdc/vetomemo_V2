export type Role = "owner" | "member" | "vet_readonly";
export type Species = "dog" | "cat" | "other";
export type HealthRecordType = "visit" | "vaccination" | "treatment";

export interface User {
  id: string;
  email: string;
  full_name: string;
  created_at: string;
}

export interface Household {
  id: string;
  name: string;
  created_at: string;
}

export interface HouseholdMembership {
  household: Household;
  role: Role;
}

export interface Animal {
  id: string;
  household_id: string;
  name: string;
  species: Species;
  breed: string | null;
  birth_date: string | null;
  created_at: string;
}

export interface HealthRecord {
  id: string;
  animal_id: string;
  type: HealthRecordType;
  title: string;
  date: string;
  vet_name: string | null;
  notes: string | null;
  details: Record<string, unknown> | null;
  created_at: string;
}

export interface WeightEntry {
  id: string;
  animal_id: string;
  weight_kg: number;
  recorded_at: string;
  created_at: string;
}

export interface Reminder {
  id: string;
  animal_id: string;
  care_type: HealthRecordType;
  title: string;
  due_date: string;
  is_done: boolean;
  created_at: string;
}