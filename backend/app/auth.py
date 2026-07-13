from collections.abc import Mapping
from datetime import datetime, timezone
import math
from typing import Any
import uuid

from pydantic import BaseModel

from app.config import Settings


class OidcClaimError(ValueError):
    """A verified token does not satisfy the GrantBridge authorization contract."""


class OidcPrincipal(BaseModel):
    subject: str
    tenant_id: uuid.UUID
    issuer: str
    audience: str


def principal_from_verified_claims(
    claims: Mapping[str, Any], settings: Settings, *, now: datetime | None = None
) -> OidcPrincipal:
    """Map already signature-verified OIDC claims to a tenant-scoped principal.

    This function deliberately does not decode or verify JWT signatures. Callers must first use
    the selected provider's discovery metadata and JWKS verifier. Keeping that boundary explicit
    prevents unsigned or merely decoded tokens from becoming authenticated sessions.
    """

    if settings.auth_mode != "oidc" or settings.oidc_issuer is None or not settings.oidc_audience:
        raise OidcClaimError("OIDC is not fully configured")

    issuer = str(claims.get("iss", ""))
    expected_issuer = str(settings.oidc_issuer)
    if issuer != expected_issuer:
        raise OidcClaimError("OIDC issuer mismatch")

    audience_claim = claims.get("aud")
    audiences = [audience_claim] if isinstance(audience_claim, str) else audience_claim
    if (
        not isinstance(audiences, list)
        or not audiences
        or not all(isinstance(audience, str) and audience for audience in audiences)
        or settings.oidc_audience not in audiences
    ):
        raise OidcClaimError("OIDC audience mismatch")

    subject = claims.get("sub")
    if not isinstance(subject, str) or not subject.strip():
        raise OidcClaimError("OIDC subject is required")

    current_time = now or datetime.now(timezone.utc)
    if current_time.tzinfo is None or current_time.utcoffset() is None:
        raise ValueError("now must be timezone-aware")
    expires_at = claims.get("exp")
    if (
        isinstance(expires_at, bool)
        or not isinstance(expires_at, (int, float))
        or not math.isfinite(expires_at)
        or expires_at <= current_time.timestamp()
    ):
        raise OidcClaimError("OIDC token is expired or has no valid expiry")

    tenant_value = claims.get(settings.oidc_tenant_claim)
    try:
        tenant_id = uuid.UUID(str(tenant_value))
    except (ValueError, TypeError, AttributeError) as error:
        raise OidcClaimError("OIDC tenant claim must be a UUID") from error

    return OidcPrincipal(
        subject=subject,
        tenant_id=tenant_id,
        issuer=issuer,
        audience=settings.oidc_audience,
    )
