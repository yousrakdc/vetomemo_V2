from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import (
    health, auth, households, animals,
    health_records, weight_entries, reminders, analysis, ws,
)

app = FastAPI(title="VetoMemo API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(households.router)
app.include_router(animals.router)
app.include_router(health_records.router)
app.include_router(weight_entries.router)
app.include_router(reminders.router)
app.include_router(analysis.router)
app.include_router(ws.router)


@app.get("/")
def root():
    return {"message": "VetoMemo API", "docs": "/docs"}