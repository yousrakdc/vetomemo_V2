"use client";

import { useEffect, useState } from "react";
import { listWeights, createWeight } from "@/lib/weights";
import { WeightEntry } from "@/lib/types";
import WeightChart from "./WeightChart";

export default function WeightsSection({
  householdId,
  animalId,
}: {
  householdId: string;
  animalId: string;
}) {
  const [weights, setWeights] = useState<WeightEntry[]>([]);
  const [weight, setWeight] = useState("");
  const [date, setDate] = useState("");
  const [saving, setSaving] = useState(false);

  async function load() {
    setWeights(await listWeights(householdId, animalId));
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [householdId, animalId]);

  async function handleAdd() {
    const value = parseFloat(weight);
    if (isNaN(value) || value <= 0 || !date) return;
    setSaving(true);
    try {
      await createWeight(householdId, animalId, { weight_kg: value, recorded_at: date });
      setWeight("");
      setDate("");
      await load();
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="card mb-6">
      <h2 className="text-xl mb-4">Courbe de poids</h2>
      <WeightChart weights={weights} />

      <div className="flex gap-3 mt-4">
        <input
          className="input"
          type="number"
          step="0.1"
          placeholder="Poids (kg)"
          value={weight}
          onChange={(e) => setWeight(e.target.value)}
        />
        <input className="input" type="date" value={date} onChange={(e) => setDate(e.target.value)} />
        <button className="btn-primary" onClick={handleAdd} disabled={saving}>
          {saving ? "..." : "Ajouter"}
        </button>
      </div>
    </div>
  );
}