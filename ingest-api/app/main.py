from fastapi import FastAPI
from pydantic import BaseModel
from .db import engine, SessionLocal, Base
from .models import Finding

app = FastAPI(title="Vuln247 Ingest")

Base.metadata.create_all(bind=engine)

class IngestPayload(BaseModel):
    tenant_id: int
    target_id: int
    tool: str
    summary: str
    raw: str

@app.post("/ingest")
def ingest(payload: IngestPayload):
    db = SessionLocal()
    f = Finding(**payload.model_dump())
    db.add(f); db.commit()
    db.close()
    return {"stored": True}