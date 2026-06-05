"use client";

import { useState } from "react";
import Link from "next/link";
import { useAuth } from "@/lib/auth-context";

export default function LoginPage() {
  const { signIn } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit() {
    setError("");
    setLoading(true);
    try {
      await signIn(email, password);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erreur de connexion");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen flex items-center justify-center p-4">
      <div className="card w-full max-w-md">
        <h1 className="text-3xl mb-1">VetoMemo</h1>
        <p className="text-sm mb-6" style={{ color: "var(--muted)" }}>
          Connectez-vous à votre carnet de santé
        </p>

        <div className="space-y-4">
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

          {error && (
            <p className="text-sm" style={{ color: "var(--danger)" }}>
              {error}
            </p>
          )}

          <button className="btn-primary w-full" onClick={handleSubmit} disabled={loading}>
            {loading ? "Connexion..." : "Se connecter"}
          </button>
        </div>

        <p className="text-sm mt-6 text-center" style={{ color: "var(--muted)" }}>
          Pas encore de compte ?{" "}
          <Link href="/register" style={{ color: "var(--sage-dark)" }}>
            Inscrivez-vous
          </Link>
        </p>
      </div>
    </main>
  );
}