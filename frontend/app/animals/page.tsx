"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import AuthGuard from "@/components/AuthGuard";
import Navbar from "@/components/Navbar";
import { useAuth } from "@/lib/auth-context";
import { listAnimals, createAnimal } from "@/lib/animals";
import { Animal, Species } from "@/lib/types";

const SPECIES_LABELS: Record<Species, string> = {
  dog: "Chien",
  cat: "Chat",
  other: "Autre",
};

function AnimalsContent() {
  const { households } = useAuth();
  const householdId = households[0]?.household.id;

  const [animals, setAnimals] = useState<Animal[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);

  // champs du formulaire
  const [name, setName] = useState("");
  const [species, setSpecies] = useState<Species>("dog");
  const [breed, setBreed] = useState("");
  const [birthDate, setBirthDate] = useState("");
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  async function load() {
    if (!householdId) return;
    setLoading(true);
    try {
      setAnimals(await listAnimals(householdId));
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [householdId]);

  async function handleCreate() {
    setError("");
    if (!name.trim()) {
      setError("Le nom est requis.");
      return;
    }
    setSaving(true);
    try {
      await createAnimal(householdId!, {
        name,
        species,
        breed: breed || null,
        birth_date: birthDate || null,
      });
      setShowModal(false);
      setName("");
      setBreed("");
      setBirthDate("");
      setSpecies("dog");
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erreur");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div>
      <Navbar />
      <main className="max-w-4xl mx-auto px-6">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-3xl">Mes animaux</h1>
          <button className="btn-primary" onClick={() => setShowModal(true)}>
            + Ajouter un animal
          </button>
        </div>

        {loading ? (
          <p style={{ color: "var(--muted)" }}>Chargement...</p>
        ) : animals.length === 0 ? (
          <div className="card text-center">
            <p style={{ color: "var(--muted)" }}>
              Aucun animal pour l'instant. Ajoutez-en un pour commencer.
            </p>
          </div>
        ) : (
          <div className="grid gap-4 sm:grid-cols-2">
            {animals.map((animal) => (
              <Link key={animal.id} href={`/animals/${animal.id}`}>
                <div className="card hover:shadow-md transition-shadow cursor-pointer">
                  <h2 className="text-xl mb-1">{animal.name}</h2>
                  <p className="text-sm" style={{ color: "var(--muted)" }}>
                    {SPECIES_LABELS[animal.species]}
                    {animal.breed ? ` · ${animal.breed}` : ""}
                  </p>
                </div>
              </Link>
            ))}
          </div>
        )}
      </main>

      {showModal && (
        <div
          className="fixed inset-0 flex items-center justify-center p-4"
          style={{ background: "rgba(45, 58, 49, 0.4)" }}
          onClick={() => setShowModal(false)}
        >
          <div className="card w-full max-w-md" onClick={(e) => e.stopPropagation()}>
            <h2 className="text-2xl mb-4">Ajouter un animal</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm mb-1">Nom</label>
                <input className="input" value={name} onChange={(e) => setName(e.target.value)} />
              </div>
              <div>
                <label className="block text-sm mb-1">Espèce</label>
                <select
                  className="input"
                  value={species}
                  onChange={(e) => setSpecies(e.target.value as Species)}
                >
                  <option value="dog">Chien</option>
                  <option value="cat">Chat</option>
                  <option value="other">Autre</option>
                </select>
              </div>
              <div>
                <label className="block text-sm mb-1">Race (optionnel)</label>
                <input className="input" value={breed} onChange={(e) => setBreed(e.target.value)} />
              </div>
              <div>
                <label className="block text-sm mb-1">Date de naissance (optionnel)</label>
                <input
                  className="input"
                  type="date"
                  value={birthDate}
                  onChange={(e) => setBirthDate(e.target.value)}
                />
              </div>

              {error && (
                <p className="text-sm" style={{ color: "var(--danger)" }}>
                  {error}
                </p>
              )}

              <div className="flex gap-3 justify-end">
                <button
                  onClick={() => setShowModal(false)}
                  className="text-sm px-4"
                  style={{ color: "var(--muted)" }}
                >
                  Annuler
                </button>
                <button className="btn-primary" onClick={handleCreate} disabled={saving}>
                  {saving ? "Ajout..." : "Ajouter"}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default function AnimalsPage() {
  return (
    <AuthGuard>
      <AnimalsContent />
    </AuthGuard>
  );
}