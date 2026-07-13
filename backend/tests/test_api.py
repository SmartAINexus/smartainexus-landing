from fastapi.testclient import TestClient

from app.config import Settings, get_settings
from app.main import app

NGO = {
    "official_name": "Asociatia Exemplu Verde",
    "registration_number": "RO-SYN-001",
    "country_code": "ro",
    "contact_email": "office@example.org",
}
GRANT = {
    "title": "Synthetic Community Programme",
    "funder": "Synthetic Foundation",
    "official_source_url": "https://example.org/grants/community",
}


def register(client: TestClient, suffix: str = "") -> dict:
    payload = NGO | {"registration_number": NGO["registration_number"] + suffix}
    response = client.post("/api/v1/ngos", json=payload)
    assert response.status_code == 201
    return response.json()


def test_register_and_read_current_ngo(client: TestClient) -> None:
    ngo = register(client)
    response = client.get("/api/v1/ngos/me", headers={"X-Tenant-ID": ngo["id"]})
    assert response.status_code == 200
    assert response.json()["country_code"] == "RO"


def test_duplicate_registration_is_safe_conflict(client: TestClient) -> None:
    register(client)
    response = client.post("/api/v1/ngos", json=NGO)
    assert response.status_code == 409
    assert response.json() == {"detail": "NGO already registered"}


def test_invalid_registration_is_rejected(client: TestClient) -> None:
    response = client.post("/api/v1/ngos", json=NGO | {"contact_email": "not-an-email"})
    assert response.status_code == 422


def test_grants_are_tenant_scoped(client: TestClient) -> None:
    first = register(client, "-A")
    second = register(client, "-B")
    created = client.post("/api/v1/grants", json=GRANT, headers={"X-Tenant-ID": first["id"]})
    assert created.status_code == 201

    visible = client.get("/api/v1/grants", headers={"X-Tenant-ID": first["id"]})
    hidden = client.get("/api/v1/grants", headers={"X-Tenant-ID": second["id"]})
    cross_tenant = client.get(f"/api/v1/grants/{created.json()['id']}",
                              headers={"X-Tenant-ID": second["id"]})
    assert len(visible.json()) == 1
    assert hidden.json() == []
    assert cross_tenant.status_code == 404
    assert cross_tenant.json() == {"detail": "Resource not found"}


def test_missing_tenant_header_is_rejected(client: TestClient) -> None:
    response = client.get("/api/v1/grants")
    assert response.status_code == 422


def test_oidc_mode_fails_closed_until_token_validation_is_wired(client: TestClient) -> None:
    app.dependency_overrides[get_settings] = lambda: Settings(
        app_env="production",
        auth_mode="oidc",
        oidc_issuer="https://identity.example.test/tenant/v2.0",
        oidc_audience="grantbridge-api",
    )
    response = client.get(
        "/api/v1/grants",
        headers={"X-Tenant-ID": "00000000-0000-0000-0000-000000000001"},
    )
    assert response.status_code == 503
    assert response.json() == {"detail": "OIDC authentication is not configured"}
