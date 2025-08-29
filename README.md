# vuln247-lite

Versión Lite (gratuita) para monitorear servicios expuestos a Internet: Nmap + SSL checks + (Nikto/Nuclei opcional) + OpenVAS sin GUI (solo backend).

## Servicios
- frontend (Next.js)
- api-gateway (FastAPI)
- ingest-api (FastAPI)
- workers: nmap, nikto, sslscan, openvas
- alerting: engine, mailer
- db: postgres_app, postgres_gvm
- redis

## Arranque rápido
1) Completar `deploy/env/*.env` desde `deploy/env/_examples/`
2) Crear el frontend con `create-next-app`
3) `docker compose up -d --build`