from fastapi import FastAPI

from app.routers import health, auth

app = FastAPI(title="VetoMemo API", version="0.1.0")

app.include_router(health.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "VetoMemo API", "docs": "/docs"}