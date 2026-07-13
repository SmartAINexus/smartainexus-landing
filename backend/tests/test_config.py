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
    settings = Settings(app_env="production", auth_mode="oidc")
    assert settings.auth_mode == "oidc"
