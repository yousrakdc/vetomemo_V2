"use client";

import { useEffect, useState, forwardRef, useImperativeHandle } from "react";
import { listReminders, toggleReminderDone, deleteReminder } from "@/lib/reminders";
import { Reminder, HealthRecordType } from "@/lib/types";

const TYPE_LABELS: Record<HealthRecordType, string> = {
  visit: "Visite",
  vaccination: "Vaccination",
  treatment: "Traitement",
};

export interface RemindersSectionHandle {
  reload: () => void;
}


interface RemindersSectionProps {
  householdId: string;
  animalId: string;
}

const RemindersSection = forwardRef<RemindersSectionHandle, RemindersSectionProps>(
  function RemindersSection({ householdId, animalId }, ref) {
  const [reminders, setReminders] = useState<Reminder[]>([]);

  async function load() {
    setReminders(await listReminders(householdId, animalId));
  }

  useImperativeHandle(ref, () => ({ reload: load }));

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [householdId, animalId]);

  async function toggle(r: Reminder) {
    await toggleReminderDone(householdId, animalId, r.id, !r.is_done);
    await load();
  }

  async function remove(id: string) {
    await deleteReminder(householdId, animalId, id);
    await load();
  }

  return (
    <div className="card mb-6">
      <h2 className="text-xl mb-4">Rappels</h2>
      {reminders.length === 0 ? (
        <p className="text-sm" style={{ color: "var(--muted)" }}>Aucun rappel.</p>
      ) : (
        <ul className="space-y-2">
          {reminders.map((r) => (
            <li key={r.id} className="flex items-center justify-between text-sm py-2"
                style={{ borderBottom: "1px solid var(--border)" }}>
              <label className="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" checked={r.is_done} onChange={() => toggle(r)} />
                <span style={{ textDecoration: r.is_done ? "line-through" : "none", color: r.is_done ? "var(--muted)" : "var(--ink)" }}>
                  {TYPE_LABELS[r.care_type]} — {r.title}{" "}
                  <span style={{ color: "var(--muted)" }}>(échéance {r.due_date})</span>
                </span>
              </label>
              <button onClick={() => remove(r.id)} style={{ color: "var(--danger)" }}>✕</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
});

export default RemindersSection;