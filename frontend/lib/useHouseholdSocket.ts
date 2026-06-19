"use client";

import { useEffect, useRef } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface HouseholdEvent {
  type: string;
  animal_id: string;
  animal_name: string;
  title?: string;
  weight_kg?: number;
}

export function useHouseholdSocket(
  householdId: string | undefined,
  onEvent: (event: HouseholdEvent) => void
) {
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!householdId) return;
    const token = window.sessionStorage.getItem("token");
    if (!token) return;

    // http://localhost:8000 -> ws://localhost:8000
    const wsUrl = API_URL.replace(/^http/, "ws");
    const ws = new WebSocket(
      `${wsUrl}/ws/households/${householdId}?token=${token}`
    );
    wsRef.current = ws;

    ws.onmessage = (e) => {
      try {
        onEvent(JSON.parse(e.data));
      } catch {
        /* ignore */
      }
    };

    return () => {
      ws.close();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [householdId]);
}