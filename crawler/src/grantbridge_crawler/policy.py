from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlsplit

from .errors import PolicyDeniedError


@dataclass(frozen=True, slots=True)
class SourceApproval:
    host: str
    approval_id: str
    official_source: bool
    terms_approved: bool
    terms_evidence: str
    robots_allowed: bool
    robots_evidence: str
    allowed_schemes: tuple[str, ...] = ("https",)
    allowed_path_prefixes: tuple[str, ...] = ("/",)


class CrawlPolicy:
    """Fail-closed pre-navigation policy for externally managed sources."""

    def __init__(self, approvals: tuple[SourceApproval, ...] | list[SourceApproval]):
        self._approvals = {item.host.lower().rstrip("."): item for item in approvals}

    def authorize(self, url: str) -> SourceApproval:
        parsed = urlsplit(url)
        host = (parsed.hostname or "").lower().rstrip(".")
        approval = self._approvals.get(host)
        if approval is None:
            raise PolicyDeniedError(f"Host is not allowlisted: {host or '<missing>'}")
        if parsed.username or parsed.password:
            raise PolicyDeniedError("Credential-bearing URLs are forbidden")
        if parsed.port not in (None, 443):
            raise PolicyDeniedError("Non-standard network ports are forbidden")
        if parsed.scheme.lower() not in approval.allowed_schemes:
            raise PolicyDeniedError(f"URL scheme is not approved: {parsed.scheme}")
        if not approval.official_source:
            raise PolicyDeniedError("Source is not recorded as official")
        if not approval.terms_approved or not approval.terms_evidence.strip():
            raise PolicyDeniedError("Terms/licence review is missing or denied")
        if not approval.robots_allowed or not approval.robots_evidence.strip():
            raise PolicyDeniedError("robots.txt review is missing or denied")
        if not any(parsed.path.startswith(prefix) for prefix in approval.allowed_path_prefixes):
            raise PolicyDeniedError(f"Path is outside the approved scope: {parsed.path}")
        return approval

