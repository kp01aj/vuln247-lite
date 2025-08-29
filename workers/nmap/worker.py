import os, json, time, subprocess, requests, redis

REDIS_URL = os.getenv("REDIS_URL","redis://redis:6379/0")
INGEST_URL = os.getenv("INGEST_URL","http://ingest:8001/ingest")

r = redis.from_url(REDIS_URL)

def parse_nmap(stdout:str) -> str:
    # Parser mínimo: contar puertos open en líneas
    open_lines = [ln for ln in stdout.splitlines() if "/tcp" in ln and "open" in ln]
    return f"Puertos abiertos detectados: {len(open_lines)}"

def run_nmap(target_value:str) -> str:
    cmd = ["nmap","-sV","--top-ports","1000","-T4",target_value]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    return res.stdout

def fetch_target_value(target_id:int) -> str:
    # Para MVP asumimos que el API no es necesario aquí; en real: consulta al API.
    # Como demo, tratamos target_id como si fuera directamente el valor.
    return str(target_id)

while True:
    job = r.brpop(["jobs:nmap"], timeout=5)
    if not job:
        time.sleep(1); continue
    _, payload = job
    data = json.loads(payload.decode())
    tenant_id = data["tenant_id"]
    target_id = data["target_id"]
    target_value = fetch_target_value(target_id)
    out = run_nmap(target_value)
    summary = parse_nmap(out)
    requests.post(INGEST_URL, json={
        "tenant_id": tenant_id,
        "target_id": target_id,
        "tool": "nmap",
        "summary": summary,
        "raw": out
    }, timeout=60)