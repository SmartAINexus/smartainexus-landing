# Backend shift handover — 2026-07-13

## Work package

FastAPI + SQLAlchemy 2 + Alembic PostgreSQL foundation with synthetic-data tests for NGO tenant
registration and tenant-scoped grant access.

## Acceptance status

- Program code: implemented under `backend/`.
- Migration: initial NGO/grant schema authored.
- Automated tests: authored but not executed because no Python runtime is exposed in the current
  shell environment.
- Production readiness: not established.

## Safety and reviewer notes

- No real personal or customer data was used.
- `.env.example` contains placeholders only; no `.env` or secret was created.
- Cross-tenant grant lookup deliberately returns the same 404 response as an absent grant.
- `X-Tenant-ID` is only a development tenant-context seam. Production must derive tenant identity
  from a trusted authentication layer; accepting a client-supplied tenant ID would be unsafe.
- PostgreSQL migration execution and downgrade still require verification against a disposable
  database.

## Next verification commands

From `backend/`, in an approved Python 3.11+ environment:

1. Install `requirements-dev.txt` in an isolated virtual environment.
2. Run `pytest`.
3. Run `alembic upgrade head` against a disposable PostgreSQL database.
4. Run `alembic downgrade base`, then `alembic upgrade head` again.
