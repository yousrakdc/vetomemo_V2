"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Scatter,
  ComposedChart,
} from "recharts";
import { WeightEntry } from "@/lib/types";

interface WeightChartProps {
  weights: WeightEntry[];
  // IDs des pesées considérées comme anormales (rempli au J10, vide pour l'instant)
  anomalyIds?: Set<string>;
}

export default function WeightChart({ weights, anomalyIds = new Set() }: WeightChartProps) {
  if (weights.length === 0) {
    return (
      <p className="text-sm" style={{ color: "var(--muted)" }}>
        Aucune pesée enregistrée. Ajoutez-en pour voir la courbe.
      </p>
    );
  }

  const data = weights.map((w) => ({
    date: w.recorded_at,
    weight: w.weight_kg,
    isAnomaly: anomalyIds.has(w.id),
    anomalyWeight: anomalyIds.has(w.id) ? w.weight_kg : null,
  }));

  return (
    <ResponsiveContainer width="100%" height={280}>
      <ComposedChart data={data} margin={{ top: 10, right: 20, bottom: 0, left: -10 }}>
        <CartesianGrid stroke="var(--border)" strokeDasharray="3 3" />
        <XAxis dataKey="date" tick={{ fontSize: 12, fill: "var(--muted)" }} />
        <YAxis
          tick={{ fontSize: 12, fill: "var(--muted)" }}
          domain={["dataMin - 1", "dataMax + 1"]}
          unit=" kg"
        />
        <Tooltip />
        <Line
          type="monotone"
          dataKey="weight"
          stroke="var(--sage)"
          strokeWidth={2}
          dot={{ r: 3, fill: "var(--sage)" }}
        />
        {/* Points d'anomalie superposés en rouge — vides tant que le J10 n'est pas fait */}
        <Scatter dataKey="anomalyWeight" fill="var(--danger)" shape="circle" />
      </ComposedChart>
    </ResponsiveContainer>
  );
}