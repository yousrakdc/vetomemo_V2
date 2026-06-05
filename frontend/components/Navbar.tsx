"use client";

import Link from "next/link";
import { useAuth } from "@/lib/auth-context";

export default function Navbar() {
  const { households, signOut } = useAuth();
  const householdName = households[0]?.household.name ?? "";

  return (
    <nav
      className="flex items-center justify-between px-6 py-4 mb-8"
      style={{ borderBottom: "1px solid var(--border)", background: "white" }}
    >
      <Link href="/animals" className="text-2xl">
        VetoMemo
      </Link>
      <div className="flex items-center gap-4">
        {householdName && (
          <span className="text-sm" style={{ color: "var(--muted)" }}>
            {householdName}
          </span>
        )}
        <button onClick={signOut} className="text-sm" style={{ color: "var(--sage-dark)" }}>
          Déconnexion
        </button>
      </div>
    </nav>
  );
}