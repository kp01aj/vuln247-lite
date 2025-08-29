import os, json, redis
from fastapi import FastAPI
from pydantic import BaseModel
from .db import engine, SessionLocal, Base
from .models import Tenant, Target

app = FastAPI(title="Vuln247 Lite API")

# Crear tablas si no existen (simple para MVP)
Base.metadata.create_all(bind=engine)

r = redis.from_url(os.getenv("REDIS_URL","redis://redis:6379/0"))

class TargetCreate(BaseModel):
    tenant_id: int
    value: str  # IP o dominio

class ScanRequest(BaseModel):
    tenant_id: int
    target_id: int
    tool: str = "nmap"

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/targets")
def add_target(payload: TargetCreate):
    db = SessionLocal()
    # Nota: validar límites del plan Lite aquí (máx 3 targets/tenant)
    t = Target(tenant_id=payload.tenant_id, value=payload.value)
    db.add(t); db.commit(); db.refresh(t)
    db.close()
    return {"id": t.id, "value": t.value}

@app.post("/scans/schedule")
def schedule_scan(req: ScanRequest):
    # Encolar job simple en Redis List por herramienta
    key = f"jobs:{req.tool}"
    job = {"tenant_id": req.tenant_id, "target_id": req.target_id}
    r.lpush(key, json.dumps(job))
    return {"queued": True, "queue": key}