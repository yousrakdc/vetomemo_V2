"use client";

import { useState } from "react";
import Link from "next/link";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";

export default function RegisterPage() {
  const { signIn } = useAuth();
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [householdName, setHouseholdName] = useState("Mon foyer");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit() {
    setError("");
    if (password.length < 8) {
      setError("Le mot de passe doit faire au moins 8 caractères.");
      return;
    }
    setLoading(true);
    try {
      await api.post("/auth/register", {
        email,
        password,
        full_name: fullName,
        household_name: householdName,
      });
      // inscription réussie → connexion automatique
      await signIn(email, password);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erreur d'inscription");
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen flex items-center justify-center p-4">
      <div className="card w-full max-w-md">
        <h1 className="text-3xl mb-1">Créer un compte</h1>
        <p className="text-sm mb-6" style={{ color: "var(--muted)" }}>
          Commencez à suivre la santé de vos animaux
        </p>

        <div className="space-y-4">
          <div>
            <label className="block text-sm mb-1">Nom complet</label>
            <input className="input" value={fullName} onChange={(e) => setFullName(e.target.value)} />
          </div>
          <div>
            <label className="block text-sm mb-1">Email</label>
            <input
              className="input"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div>
            <label className="block text-sm mb-1">Mot de passe</label>
            <input
              className="input"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <div>
            <label className="block text-sm mb-1">Nom du foyer</label>
            <input
              className="input"
              value={householdName}
              onChange={(e) => setHouseholdName(e.target.value)}
            />
          </div>

          {error && (
            <p className="text-sm" style={{ color: "var(--danger)" }}>
              {error}
            </p>
          )}

          <button className="btn-primary w-full" onClick={handleSubmit} disabled={loading}>
            {loading ? "Création..." : "Créer mon compte"}
          </button>
        </div>

        <p className="text-sm mt-6 text-center" style={{ color: "var(--muted)" }}>
          Déjà inscrit ?{" "}
          <Link href="/login" style={{ color: "var(--sage-dark)" }}>
            Connectez-vous
          </Link>
        </p>
      </div>
    </main>
  );
}