import { api } from "./api";
import { Reminder } from "./types";

const base = (h: string, a: string) =>
  `/households/${h}/animals/${a}/reminders`;

export function listReminders(h: string, a: string) {
  return api.get<Reminder[]>(base(h, a));
}

export function toggleReminderDone(h: string, a: string, id: string, isDone: boolean) {
  return api.patch<Reminder>(`${base(h, a)}/${id}`, { is_done: isDone });
}

export function deleteReminder(h: string, a: string, id: string) {
  return api.delete<void>(`${base(h, a)}/${id}`);
}