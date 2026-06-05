from fastapi import FastAPI

from app.routers import (
    health, auth, households, animals,
    health_records, weight_entries, reminders,
)

app = FastAPI(title="VetoMemo API", version="0.1.0")

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(households.router)
app.include_router(animals.router)
app.include_router(health_records.router)
app.include_router(weight_entries.router)
app.include_router(reminders.router)


@app.get("/")
def root():
    return {"message": "VetoMemo API", "docs": "/docs"}