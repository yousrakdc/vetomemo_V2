"use client";

import { useEffect, useState } from "react";
import { listWeights, createWeight } from "@/lib/weights";
import { analyzeWeight, WeightAnalysis } from "@/lib/analysis";
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
  const [analysis, setAnalysis] = useState<WeightAnalysis | null>(null);
  const [weight, setWeight] = useState("");
  const [date, setDate] = useState("");
  const [saving, setSaving] = useState(false);

  async function load() {
    const w = await listWeights(householdId, animalId);
    setWeights(w);
    try {
      setAnalysis(await analyzeWeight(householdId, animalId));
    } catch {
      setAnalysis(null);
    }
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

  const anomalyIds = new Set(analysis?.anomalies.anomaly_ids ?? []);
  const trend = analysis?.trend;

  return (
    <div className="card mb-6">
      <h2 className="text-xl mb-4">Courbe de poids</h2>
      <WeightChart weights={weights} anomalyIds={anomalyIds} />

      {trend?.enough_data && (
        <div
          className="mt-4 p-3 text-sm rounded-lg"
          style={{ background: "var(--sage-tint)", color: "var(--sage-dark)" }}
        >
          Tendance :{" "}
          {trend.direction === "hausse"
            ? "le poids est en hausse"
            : trend.direction === "baisse"
            ? "le poids est en baisse"
            : "le poids est stable"}
          {trend.projected_weight_30d != null &&
            ` — projection à 30 jours : ${trend.projected_weight_30d} kg`}
          .
        </div>
      )}

      {anomalyIds.size > 0 && (
        <div
          className="mt-2 p-3 text-sm rounded-lg"
          style={{ background: "var(--danger-tint)", color: "var(--danger)" }}
        >
          {anomalyIds.size} pesée(s) s'écarte(nt) nettement de la moyenne (points rouges sur la
          courbe). Une vérification peut être utile.
        </div>
      )}

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
