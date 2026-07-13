# GrantBridge Europe backend

FastAPI, SQLAlchemy 2 and Alembic foundation for PostgreSQL. Development and tests use
synthetic data only.

## Local setup

1. Create a virtual environment and install `requirements-dev.txt`.
2. Copy `.env.example` to `.env` and replace the placeholder database credentials locally.
3. Run `alembic upgrade head`.
4. Start with `uvicorn app.main:app --reload`.
5. Run `pytest` for the isolated API tests.

`X-Tenant-ID` is an interim tenant-context mechanism, not production authentication. A trusted
identity provider must supply tenant context before production launch; clients must not be allowed
to assert arbitrary tenant identifiers.
