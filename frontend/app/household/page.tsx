"use client";

import { useEffect, useState } from "react";
import AuthGuard from "@/components/AuthGuard";
import Navbar from "@/components/Navbar";
import { useAuth } from "@/lib/auth-context";
import { listMembers, addMember, removeMember, Member } from "@/lib/members";
import { Role } from "@/lib/types";

const ROLE_LABELS: Record<Role, string> = {
  owner: "Propriétaire",
  member: "Membre du foyer",
  vet_readonly: "Vétérinaire (lecture seule)",
};

function HouseholdContent() {
  const { households } = useAuth();
  const householdId = households[0]?.household.id;
  const myRole = households[0]?.role;

  const [members, setMembers] = useState<Member[]>([]);
  const [email, setEmail] = useState("");
  const [role, setRole] = useState<Role>("member");
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  async function load() {
    if (!householdId) return;
    setMembers(await listMembers(householdId));
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [householdId]);

  async function handleAdd() {
    setError("");
    if (!email.trim()) {
      setError("Email requis.");
      return;
    }
    setSaving(true);
    try {
      await addMember(householdId!, email, role);
      setEmail("");
      setRole("member");
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erreur");
    } finally {
      setSaving(false);
    }
  }

  async function handleRemove(membershipId: string) {
    if (!confirm("Retirer ce membre du foyer ?")) return;
    await removeMember(householdId!, membershipId);
    await load();
  }

  const isOwner = myRole === "owner";

  return (
    <div>
      <Navbar />
      <main className="max-w-3xl mx-auto px-6">
        <h1 className="text-3xl mb-6">Mon foyer</h1>

        <div className="card mb-6">
          <h2 className="text-xl mb-4">Membres</h2>
          <ul className="space-y-2">
            {members.map((m) => (
              <li
                key={m.membership_id}
                className="flex items-center justify-between py-2 text-sm"
                style={{ borderBottom: "1px solid var(--border)" }}
              >
                <div>
                  <span style={{ fontWeight: 600 }}>{m.user_name}</span>{" "}
                  <span style={{ color: "var(--muted)" }}>({m.user_email})</span>
                  <span
                    className="ml-2 px-2 py-0.5 rounded-full text-xs"
                    style={{ background: "var(--sage-tint)", color: "var(--sage-dark)" }}
                  >
                    {ROLE_LABELS[m.role]}
                  </span>
                </div>
                {isOwner && m.role !== "owner" && (
                  <button onClick={() => handleRemove(m.membership_id)} style={{ color: "var(--danger)" }}>
                    Retirer
                  </button>
                )}
              </li>
            ))}
          </ul>
        </div>

        {isOwner && (
          <div className="card">
            <h2 className="text-xl mb-4">Inviter un membre</h2>
            <p className="text-sm mb-4" style={{ color: "var(--muted)" }}>
              La personne doit déjà avoir un compte VetoMemo.
            </p>
            <div className="space-y-3">
              <input
                className="input"
                type="email"
                placeholder="Email de la personne"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              <select className="input" value={role} onChange={(e) => setRole(e.target.value as Role)}>
                <option value="member">Membre du foyer</option>
                <option value="vet_readonly">Vétérinaire (lecture seule)</option>
              </select>
              {error && (
                <p className="text-sm" style={{ color: "var(--danger)" }}>
                  {error}
                </p>
              )}
              <button className="btn-primary" onClick={handleAdd} disabled={saving}>
                {saving ? "Ajout..." : "Inviter"}
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default function HouseholdPage() {
  return (
    <AuthGuard>
      <HouseholdContent />
    </AuthGuard>
  );
}