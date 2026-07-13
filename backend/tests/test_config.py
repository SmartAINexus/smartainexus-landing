import pytest
from pydantic import ValidationError

from app.config import Settings


def test_development_header_is_allowed_only_outside_production() -> None:
    settings = Settings(app_env="development", auth_mode="development_header")
    assert settings.auth_mode == "development_header"


def test_production_rejects_untrusted_tenant_header_auth() -> None:
    with pytest.raises(ValidationError, match="Production cannot use"):
        Settings(app_env="production", auth_mode="development_header")


def test_production_accepts_oidc_auth_mode() -> None:
    settings = Settings(
        app_env="production",
        auth_mode="oidc",
        oidc_issuer="https://identity.example.test/tenant/v2.0",
        oidc_audience="grantbridge-api",
    )
    assert settings.auth_mode == "oidc"


def test_oidc_mode_requires_https_issuer_and_audience() -> None:
    with pytest.raises(ValidationError, match="requires OIDC_ISSUER"):
        Settings(auth_mode="oidc")
    with pytest.raises(ValidationError, match="must use HTTPS"):
        Settings(
            auth_mode="oidc",
            oidc_issuer="http://identity.example.test/tenant/v2.0",
            oidc_audience="grantbridge-api",
        )
    with pytest.raises(ValidationError, match="query or fragment"):
        Settings(
            auth_mode="oidc",
            oidc_issuer="https://identity.example.test/tenant/v2.0?unsafe=true",
            oidc_audience="grantbridge-api",
        )
