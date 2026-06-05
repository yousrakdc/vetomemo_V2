"use client";

import { useEffect, useState } from "react";
import {
  listHealthRecords,
  createHealthRecord,
  deleteHealthRecord,
} from "@/lib/health";
import { HealthRecord, HealthRecordType } from "@/lib/types";

const TYPE_LABELS: Record<HealthRecordType, string> = {
  visit: "Visite",
  vaccination: "Vaccination",
  treatment: "Traitement",
};

export default function HealthRecordsSection({
  householdId,
  animalId,
  onChange,
}: {
  householdId: string;
  animalId: string;
  onChange?: () => void;
}) {
  const [records, setRecords] = useState<HealthRecord[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [type, setType] = useState<HealthRecordType>("vaccination");
  const [title, setTitle] = useState("");
  const [date, setDate] = useState("");
  const [vetName, setVetName] = useState("");
  const [saving, setSaving] = useState(false);

  async function load() {
    setRecords(await listHealthRecords(householdId, animalId));
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [householdId, animalId]);

  async function handleAdd() {
    if (!title.trim() || !date) return;
    setSaving(true);
    try {
      await createHealthRecord(householdId, animalId, {
        type,
        title,
        date,
        vet_name: vetName || null,
        create_reminder: true,
      });
      setTitle("");
      setDate("");
      setVetName("");
      setShowForm(false);
      await load();
      onChange?.(); // pour rafraîchir les rappels générés automatiquement
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete(id: string) {
    await deleteHealthRecord(householdId, animalId, id);
    await load();
  }

  return (
    <div className="card mb-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl">Soins</h2>
        <button
          className="text-sm"
          style={{ color: "var(--sage-dark)" }}
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? "Annuler" : "+ Ajouter"}
        </button>
      </div>

      {showForm && (
        <div className="space-y-3 mb-4 pb-4" style={{ borderBottom: "1px solid var(--border)" }}>
          <select className="input" value={type} onChange={(e) => setType(e.target.value as HealthRecordType)}>
            <option value="vaccination">Vaccination</option>
            <option value="visit">Visite</option>
            <option value="treatment">Traitement</option>
          </select>
          <input className="input" placeholder="Intitulé" value={title} onChange={(e) => setTitle(e.target.value)} />
          <input className="input" type="date" value={date} onChange={(e) => setDate(e.target.value)} />
          <input className="input" placeholder="Vétérinaire (optionnel)" value={vetName} onChange={(e) => setVetName(e.target.value)} />
          <button className="btn-primary w-full" onClick={handleAdd} disabled={saving}>
            {saving ? "Ajout..." : "Enregistrer le soin"}
          </button>
        </div>
      )}

      {records.length === 0 ? (
        <p className="text-sm" style={{ color: "var(--muted)" }}>Aucun soin enregistré.</p>
      ) : (
        <ul className="space-y-2">
          {records.map((r) => (
            <li key={r.id} className="flex items-center justify-between text-sm py-2"
                style={{ borderBottom: "1px solid var(--border)" }}>
              <div>
                <span style={{ color: "var(--sage-dark)", fontWeight: 600 }}>
                  {TYPE_LABELS[r.type]}
                </span>{" "}
                — {r.title} <span style={{ color: "var(--muted)" }}>({r.date})</span>
              </div>
              <button onClick={() => handleDelete(r.id)} style={{ color: "var(--danger)" }}>
                ✕
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}