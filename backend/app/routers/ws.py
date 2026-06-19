import uuid

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from sqlalchemy import select

from app.core.database import SessionLocal
from app.core.security import decode_access_token
from app.core.ws_manager import manager
from app.models.membership import Membership

router = APIRouter(tags=["websocket"])


@router.websocket("/ws/households/{household_id}")
async def household_ws(
    websocket: WebSocket,
    household_id: uuid.UUID,
    token: str = Query(...),
):
    # Authentification via le token passé en query param
    subject = decode_access_token(token)
    if subject is None:
        await websocket.close(code=4401)  # unauthorized
        return

    # Vérifie que l'utilisateur appartient bien au foyer
    db = SessionLocal()
    try:
        user_id = uuid.UUID(subject)
        membership = db.scalar(
            select(Membership).where(
                Membership.user_id == user_id,
                Membership.household_id == household_id,
            )
        )
    finally:
        db.close()

    if membership is None:
        await websocket.close(code=4403)  # forbidden
        return

    hid = str(household_id)
    await manager.connect(hid, websocket)
    try:
        while True:
            # On garde la connexion ouverte ; on ignore les messages entrants
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(hid, websocket)
    