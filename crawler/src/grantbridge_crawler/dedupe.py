from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from .models import FundingOpportunity

_TRACKING_KEYS = {"fbclid", "gclid", "mc_cid", "mc_eid"}


def _text(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).casefold()
    return re.sub(r"\s+", " ", normalized).strip()


def canonical_url(value: str) -> str:
    parsed = urlsplit(value)
    host = (parsed.hostname or "").lower().rstrip(".")
    port = f":{parsed.port}" if parsed.port and parsed.port != 443 else ""
    path = re.sub(r"/{2,}", "/", parsed.path or "/")
    if path != "/":
        path = path.rstrip("/")
    query = [
        (key, val)
        for key, val in parse_qsl(parsed.query, keep_blank_values=True)
        if not key.lower().startswith("utm_") and key.lower() not in _TRACKING_KEYS
    ]
    return urlunsplit((parsed.scheme.lower(), host + port, path, urlencode(sorted(query)), ""))


def content_hash(opportunity: FundingOpportunity) -> str:
    payload = {
        "title": _text(opportunity.title),
        "deadline": opportunity.deadline.isoformat(),
        "timezone": _text(opportunity.timezone),
        "eligibility": sorted({_text(item) for item in opportunity.eligibility}),
        "source_url": canonical_url(opportunity.source_url),
    }
    serialized = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

