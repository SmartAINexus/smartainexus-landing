from datetime import datetime, timezone
import uuid

import pytest

from app.auth import OidcClaimError, principal_from_verified_claims
from app.config import Settings


NOW = datetime(2026, 7, 13, 3, 30, tzinfo=timezone.utc)
TENANT_ID = uuid.UUID("11111111-1111-4111-8111-111111111111")


@pytest.fixture
def oidc_settings() -> Settings:
    return Settings(
        app_env="production",
        auth_mode="oidc",
        oidc_issuer="https://identity.example.test/tenant/v2.0",
        oidc_audience="grantbridge-api",
    )


def claims(**updates: object) -> dict[str, object]:
    values: dict[str, object] = {
        "iss": "https://identity.example.test/tenant/v2.0",
        "aud": "grantbridge-api",
        "sub": "synthetic-user-1",
        "exp": NOW.timestamp() + 600,
        "grantbridge_tenant_id": str(TENANT_ID),
    }
    values.update(updates)
    return values


def test_verified_claims_map_to_tenant_principal(oidc_settings: Settings) -> None:
    principal = principal_from_verified_claims(claims(), oidc_settings, now=NOW)

    assert principal.subject == "synthetic-user-1"
    assert principal.tenant_id == TENANT_ID
    assert principal.audience == "grantbridge-api"


@pytest.mark.parametrize(
    ("updates", "message"),
    [
        ({"iss": "https://attacker.example.test"}, "issuer mismatch"),
        ({"iss": "https://identity.example.test/tenant/v2.0/"}, "issuer mismatch"),
        ({"aud": "different-api"}, "audience mismatch"),
        ({"aud": ["different-api", "another-api"]}, "audience mismatch"),
        ({"aud": ["grantbridge-api", 123]}, "audience mismatch"),
        ({"aud": []}, "audience mismatch"),
        ({"aud": {"value": "grantbridge-api"}}, "audience mismatch"),
        ({"sub": ""}, "subject is required"),
        ({"exp": NOW.timestamp()}, "expired"),
        ({"exp": None}, "expired"),
        ({"exp": True}, "expired"),
        ({"exp": float("nan")}, "expired"),
        ({"exp": float("inf")}, "expired"),
        ({"grantbridge_tenant_id": "not-a-uuid"}, "tenant claim"),
    ],
)
def test_claim_contract_fails_closed(
    oidc_settings: Settings, updates: dict[str, object], message: str
) -> None:
    with pytest.raises(OidcClaimError, match=message):
        principal_from_verified_claims(claims(**updates), oidc_settings, now=NOW)


def test_audience_array_is_supported(oidc_settings: Settings) -> None:
    principal = principal_from_verified_claims(
        claims(aud=["another-api", "grantbridge-api"]), oidc_settings, now=NOW
    )
    assert principal.tenant_id == TENANT_ID


def test_development_mode_cannot_map_oidc_claims() -> None:
    settings = Settings(app_env="development", auth_mode="development_header")
    with pytest.raises(OidcClaimError, match="not fully configured"):
        principal_from_verified_claims(claims(), settings, now=NOW)


def test_custom_tenant_claim_name_is_enforced() -> None:
    settings = Settings(
        auth_mode="oidc",
        oidc_issuer="https://identity.example.test/tenant/v2.0",
        oidc_audience="grantbridge-api",
        oidc_tenant_claim="organisation_id",
    )
    custom_claims = claims(organisation_id=str(TENANT_ID))

    principal = principal_from_verified_claims(custom_claims, settings, now=NOW)
    assert principal.tenant_id == TENANT_ID

    missing_custom = claims()
    missing_custom.pop("organisation_id", None)
    with pytest.raises(OidcClaimError, match="tenant claim"):
        principal_from_verified_claims(missing_custom, settings, now=NOW)
