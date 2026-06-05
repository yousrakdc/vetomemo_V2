"use client";

import { createContext, useContext, useEffect, useState, ReactNode } from "react";
import { useRouter } from "next/navigation";
import { login as apiLogin, setToken, clearToken, api } from "./api";
import { HouseholdMembership } from "./types";

interface AuthState {
  isAuthenticated: boolean;
  households: HouseholdMembership[];
  loading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signOut: () => void;
  refreshHouseholds: () => Promise<void>;
}

const AuthContext = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [households, setHouseholds] = useState<HouseholdMembership[]>([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  async function refreshHouseholds() {
    try {
      const data = await api.get<HouseholdMembership[]>("/households/mine");
      setHouseholds(data);
    } catch {
      setHouseholds([]);
    }
  }

  useEffect(() => {
    const token = window.sessionStorage.getItem("token");
    if (token) {
      setIsAuthenticated(true);
      refreshHouseholds().finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  async function signIn(email: string, password: string) {
    const token = await apiLogin(email, password);
    setToken(token);
    setIsAuthenticated(true);
    await refreshHouseholds();
    router.push("/animals");
  }

  function signOut() {
    clearToken();
    setIsAuthenticated(false);
    setHouseholds([]);
    router.push("/login");
  }

  return (
    <AuthContext.Provider
      value={{ isAuthenticated, households, loading, signIn, signOut, refreshHouseholds }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth doit être utilisé dans AuthProvider");
  return ctx;
}