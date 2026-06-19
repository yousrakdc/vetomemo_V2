"use client";

import { useEffect, useRef, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import AuthGuard from "@/components/AuthGuard";
import Navbar from "@/components/Navbar";
import { useAuth } from "@/lib/auth-context";
import { getAnimal, deleteAnimal } from "@/lib/animals";
import { Animal, Species } from "@/lib/types";
import HealthRecordsSection from "@/components/HealthRecordsSection";
import WeightsSection from "@/components/WeightsSection";
import RemindersSection, { RemindersSectionHandle } from "@/components/RemindersSection";
import ProfileSection from "@/components/ProfileSection";

const SPECIES_LABELS: Record<Species, string> = {
  dog: "Chien",
  cat: "Chat",
  other: "Autre",
};

function AnimalDetailContent() {
  const params = useParams();
  const router = useRouter();
  const { activeHousehold } = useAuth();
  const householdId = activeHousehold?.household.id;
  const myRole = activeHousehold?.role;
  const animalId = params.id as string;

  const [animal, setAnimal] = useState<Animal | null>(null);
  const [loading, setLoading] = useState(true);
  const remindersRef = useRef<RemindersSectionHandle>(null);

  useEffect(() => {
    if (!householdId) return;
    getAnimal(householdId, animalId)
      .then(setAnimal)
      .finally(() => setLoading(false));
  }, [householdId, animalId]);

  async function handleDelete() {
    if (!confirm("Supprimer cet animal et tout son historique ?")) return;
    await deleteAnimal(householdId!, animalId);
    router.push("/animals");
  }

  return (
    <div>
      <Navbar />
      <main className="max-w-4xl mx-auto px-6 pb-12">
        <button onClick={() => router.push("/animals")} className="text-sm mb-4" style={{ color: "var(--sage-dark)" }}>
          ← Retour
        </button>

        {loading ? (
          <p style={{ color: "var(--muted)" }}>Chargement...</p>
        ) : !animal ? (
          <p style={{ color: "var(--danger)" }}>Animal introuvable.</p>
        ) : (
          <div>
            <div className="flex items-center justify-between mb-6">
              <div>
                <h1 className="text-3xl mb-1">{animal.name}</h1>
                <p style={{ color: "var(--muted)" }}>
                  {SPECIES_LABELS[animal.species]}
                  {animal.breed ? ` · ${animal.breed}` : ""}
                </p>
              </div>
              <button onClick={handleDelete} className="text-sm" style={{ color: "var(--danger)" }}>
                Supprimer
              </button>
            </div>

            {householdId && (
              <>
                <RemindersSection ref={remindersRef} householdId={householdId} animalId={animalId} />
                <ProfileSection householdId={householdId} animalId={animalId} />
                <HealthRecordsSection
                  householdId={householdId}
                  animalId={animalId}
                  onChange={() => remindersRef.current?.reload()}
                />
                <WeightsSection householdId={householdId} animalId={animalId} />
              </>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default function AnimalDetailPage() {
  return (
    <AuthGuard>
      <AnimalDetailContent />
    </AuthGuard>
  );
}