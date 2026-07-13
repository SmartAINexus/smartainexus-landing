from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True, slots=True)
class Provenance:
    source_url: str
    retrieved_at: datetime
    parser_name: str
    parser_version: str
    official_source: bool
    allowlist_approval_id: str
    robots_evidence: str
    terms_evidence: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "source_url": self.source_url,
            "retrieved_at": self.retrieved_at.isoformat(),
            "parser_name": self.parser_name,
            "parser_version": self.parser_version,
            "official_source": self.official_source,
            "allowlist_approval_id": self.allowlist_approval_id,
            "robots_evidence": self.robots_evidence,
            "terms_evidence": self.terms_evidence,
        }


@dataclass(frozen=True, slots=True)
class FundingOpportunity:
    title: str
    funder: str
    description: str
    deadline: datetime
    timezone: str
    eligibility: tuple[str, ...]
    source_url: str
    provenance: Provenance
    normalized_hash: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "funder": self.funder,
            "description": self.description,
            "deadline": self.deadline.isoformat(),
            "timezone": self.timezone,
            "eligibility": list(self.eligibility),
            "source_url": self.source_url,
            "provenance": self.provenance.as_dict(),
            "normalized_hash": self.normalized_hash,
        }

    def as_ingest_payload(self) -> dict[str, Any]:
        """Return the versioned backend ingestion contract without tenant data."""

        return {
            "normalized_hash": self.normalized_hash,
            "title": self.title,
            "funder": self.funder,
            "description": self.description,
            "eligibility": list(self.eligibility),
            "official_source_url": self.source_url,
            "deadline": self.deadline.isoformat(),
            "timezone": self.timezone,
            "provenance": self.provenance.as_dict(),
        }
