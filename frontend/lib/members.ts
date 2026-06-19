import { api } from "./api";
import { Role } from "./types";

export interface Member {
  membership_id: string;
  user_email: string;
  user_name: string;
  role: Role;
}

export function listMembers(householdId: string) {
  return api.get<Member[]>(`/households/${householdId}/members`);
}

export function addMember(householdId: string, email: string, role: Role) {
  return api.post<Member>(`/households/${householdId}/members`, { email, role });
}

export function removeMember(householdId: string, membershipId: string) {
  return api.delete<void>(`/households/${householdId}/members/${membershipId}`);
}