"use client";

import { useEffect, useState } from "react";
import { getAnimalProfile, AnimalProfile } from "@/lib/analysis";

export default function ProfileSection({
  householdId,
  animalId,
}: {
  householdId: string;
  animalId: string;
}) {
  const [profile, setProfile] = useState<AnimalProfile | null>(null);

  useEffect(() => {
    getAnimalProfile(householdId, animalId)
      .then(setProfile)
      .catch(() => setProfile(null));
  }, [householdId, animalId]);

  if (!profile) return null;

  return (
    <div className="card mb-6">
      <h2 className="text-xl mb-4">Profil de soins préventifs</h2>

      {!profile.available ? (
        <p className="text-sm" style={{ color: "var(--muted)" }}>
          {profile.reason}
        </p>
      ) : (
        <div>
          <div
            className="inline-block mb-3 px-3 py-1 rounded-full text-sm"
            style={{ background: "var(--sage-tint)", color: "var(--sage-dark)", fontWeight: 600 }}
          >
            {profile.profile_label}
          </div>
          <p className="text-sm mb-2" style={{ color: "var(--muted)" }}>
            Soins préventifs suggérés pour ce profil :
          </p>
          <ul className="space-y-1">
            {profile.suggested_care.map((care, i) => (
              <li key={i} className="text-sm flex items-start gap-2">
                <span style={{ color: "var(--sage)" }}>•</span>
                {care}
              </li>
            ))}
          </ul>
          <p className="text-xs mt-3" style={{ color: "var(--muted)", fontStyle: "italic" }}>
            Profil déterminé par regroupement (k-means) à partir de l'âge et du poids.
            Ces suggestions ne remplacent pas l'avis d'un vétérinaire.
          </p>
        </div>
      )}
    </div>
  );
}
