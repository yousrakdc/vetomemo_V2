"""Gestionnaire de connexions WebSocket avec diffusion via Redis pub/sub.

Chaque foyer a un canal Redis ("household:{id}"). Quand un événement survient,
il est publié sur le canal du foyer ; toutes les instances backend abonnées le
reçoivent et le transmettent aux clients WebSocket connectés qu'elles gèrent.
Cette indirection par Redis permet le passage à l'échelle multi-instances.
"""
import asyncio
import json
from collections import defaultdict

import redis.asyncio as aioredis
from fastapi import WebSocket

from app.core.config import settings


class ConnectionManager:
    def __init__(self) -> None:
        # foyer -> ensemble des websockets connectés sur CETTE instance
        self.active: dict[str, set[WebSocket]] = defaultdict(set)
        self._redis: aioredis.Redis | None = None
        self._pubsub_task: asyncio.Task | None = None

    async def _get_redis(self) -> aioredis.Redis:
        if self._redis is None:
            self._redis = aioredis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                decode_responses=True,
            )
        return self._redis

    async def connect(self, household_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active[household_id].add(websocket)
        # Démarre l'écoute Redis globale au premier client
        if self._pubsub_task is None:
            self._pubsub_task = asyncio.create_task(self._listen_redis())

    def disconnect(self, household_id: str, websocket: WebSocket) -> None:
        self.active[household_id].discard(websocket)

    async def publish(self, household_id: str, message: dict) -> None:
        """Publie un événement sur le canal Redis du foyer."""
        redis = await self._get_redis()
        await redis.publish(f"household:{household_id}", json.dumps(message))

    async def _listen_redis(self) -> None:
        """Écoute tous les canaux de foyers et relaie aux websockets locaux."""
        redis = await self._get_redis()
        pubsub = redis.pubsub()
        await pubsub.psubscribe("household:*")
        async for raw in pubsub.listen():
            if raw["type"] != "pmessage":
                continue
            channel = raw["channel"]  # "household:{id}"
            household_id = channel.split(":", 1)[1]
            message = raw["data"]
            # Transmet à tous les websockets de ce foyer sur cette instance
            dead = set()
            for ws in self.active.get(household_id, set()):
                try:
                    await ws.send_text(message)
                except Exception:
                    dead.add(ws)
            for ws in dead:
                self.active[household_id].discard(ws)


manager = ConnectionManager()