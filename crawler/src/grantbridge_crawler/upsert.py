from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol

from .models import FundingOpportunity


class UpsertResult(str, Enum):
    INSERTED = "inserted"
    UNCHANGED = "unchanged"
    UPDATED = "updated"


class OpportunityRepository(Protocol):
    async def upsert(self, opportunity: FundingOpportunity) -> UpsertResult: ...


@dataclass(slots=True)
class InMemoryOpportunityRepository:
    """Deterministic test/reference repository; production storage is injected."""

    records: dict[str, FundingOpportunity]

    def __init__(self) -> None:
        self.records = {}

    async def upsert(self, opportunity: FundingOpportunity) -> UpsertResult:
        existing = self.records.get(opportunity.normalized_hash)
        if existing == opportunity:
            return UpsertResult.UNCHANGED
        self.records[opportunity.normalized_hash] = opportunity
        return UpsertResult.UPDATED if existing else UpsertResult.INSERTED

