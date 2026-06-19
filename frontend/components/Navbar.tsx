"use client";

import Link from "next/link";
import { useAuth } from "@/lib/auth-context";

export default function Navbar() {
  const { households, activeHousehold, setActiveHouseholdId, signOut } = useAuth();

  return (
    <nav
      className="flex items-center justify-between px-6 py-4 mb-8"
      style={{ borderBottom: "1px solid var(--border)", background: "white" }}
    >
      <Link href="/animals" className="text-2xl">
        VetoMemo
      </Link>
      <div className="flex items-center gap-4">
        {households.length > 1 ? (
          <select
            className="text-sm"
            style={{
              border: "1px solid var(--border)",
              borderRadius: "0.4rem",
              padding: "0.3rem 0.5rem",
              background: "white",
            }}
            value={activeHousehold?.household.id ?? ""}
            onChange={(e) => setActiveHouseholdId(e.target.value)}
          >
            {households.map((h) => (
              <option key={h.household.id} value={h.household.id}>
                {h.household.name}
              </option>
            ))}
          </select>
        ) : (
          activeHousehold && (
            <Link href="/household" className="text-sm" style={{ color: "var(--muted)" }}>
              {activeHousehold.household.name}
            </Link>
          )
        )}
        <Link href="/household" className="text-sm" style={{ color: "var(--sage-dark)" }}>
          Foyer
        </Link>
        <button onClick={signOut} className="text-sm" style={{ color: "var(--sage-dark)" }}>
          Déconnexion
        </button>
      </div>
    </nav>
  );
}