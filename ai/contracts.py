from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Mapping, Sequence


class EvidenceState(StrEnum):
    VERIFIED = "verified"
    LIKELY = "likely"
    NEEDS_REVIEW = "needs_review"
    EXCLUSION_RISK = "exclusion_risk"


@dataclass(frozen=True)
class MatchInput:
    tenant_id: str
    ngo_focus_areas: Sequence[str]
    operating_countries: Sequence[str]
    project_summary: str
    grant_id: str
    grant_description: str
    verified_eligibility: Mapping[str, str]

    def __post_init__(self) -> None:
        if not self.tenant_id or not self.grant_id:
            raise ValueError("tenant_id and grant_id are required")
        if not self.ngo_focus_areas:
            raise ValueError("at least one NGO focus area is required")


@dataclass(frozen=True)
class MatchFactor:
    name: str
    score: int
    rationale: str
    evidence_state: EvidenceState
    source_reference: str | None = None

    def __post_init__(self) -> None:
        if not 0 <= self.score <= 100:
            raise ValueError("factor score must be between 0 and 100")


@dataclass(frozen=True)
class MatchResult:
    score: int
    factors: Sequence[MatchFactor] = field(default_factory=tuple)
    missing_information: Sequence[str] = field(default_factory=tuple)
    exclusion_risks: Sequence[str] = field(default_factory=tuple)
    requires_human_review: bool = True

    def __post_init__(self) -> None:
        if not 0 <= self.score <= 100:
            raise ValueError("match score must be between 0 and 100")
        if self.exclusion_risks and not self.requires_human_review:
            raise ValueError("exclusion risks always require human review")

