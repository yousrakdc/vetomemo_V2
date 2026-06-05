import { api } from "./api";
import { HealthRecord, HealthRecordType } from "./types";

export interface HealthRecordInput {
  type: HealthRecordType;
  title: string;
  date: string;
  vet_name?: string | null;
  notes?: string | null;
  create_reminder?: boolean;
}

const base = (h: string, a: string) =>
  `/households/${h}/animals/${a}/health-records`;

export function listHealthRecords(h: string, a: string) {
  return api.get<HealthRecord[]>(base(h, a));
}

export function createHealthRecord(h: string, a: string, data: HealthRecordInput) {
  return api.post<HealthRecord>(base(h, a), data);
}

export function deleteHealthRecord(h: string, a: string, id: string) {
  return api.delete<void>(`${base(h, a)}/${id}`);
}