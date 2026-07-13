from dataclasses import replace
import asyncio
from datetime import datetime, timezone

from grantbridge_crawler.dedupe import canonical_url, content_hash
from grantbridge_crawler.models import FundingOpportunity, Provenance
from grantbridge_crawler.upsert import InMemoryOpportunityRepository, UpsertResult


def opportunity(**changes: object) -> FundingOpportunity:
    provenance = Provenance(
        source_url="https://funding.example.test/calls/green",
        retrieved_at=datetime(2026, 7, 13, tzinfo=timezone.utc),
        parser_name="fixture",
        parser_version="1",
        official_source=True,
        allowlist_approval_id="fixture",
        robots_evidence="fixture",
        terms_evidence="fixture",
    )
    base = FundingOpportunity(
        title="Community Green Transition",
        funder="Synthetic Romanian Public Authority",
        description="Synthetic programme description",
        deadline=datetime.fromisoformat("2026-09-30T17:00:00+03:00"),
        timezone="Europe/Bucharest",
        eligibility=("Romanian nonprofits", "Registered organisations"),
        source_url="https://funding.example.test/calls/green?utm_source=test",
        provenance=provenance,
    )
    return replace(base, **changes)


def test_hash_normalizes_whitespace_case_tracking_and_eligibility_order() -> None:
    first = opportunity()
    second = opportunity(
        title="  COMMUNITY   GREEN transition ",
        eligibility=("Registered organisations", "Romanian nonprofits"),
        source_url="https://FUNDING.example.test/calls/green/",
    )
    assert content_hash(first) == content_hash(second)


def test_hash_changes_when_deadline_changes() -> None:
    changed = opportunity(deadline=datetime.fromisoformat("2026-10-01T17:00:00+03:00"))
    assert content_hash(opportunity()) != content_hash(changed)


def test_canonical_url_drops_fragment_and_tracking() -> None:
    assert canonical_url("https://EXAMPLE.test/a/?utm_campaign=x&b=2#a") == "https://example.test/a?b=2"


def test_repository_deduplicates_by_normalized_hash() -> None:
    repo = InMemoryOpportunityRepository()
    item = opportunity()
    item = replace(item, normalized_hash=content_hash(item))
    async def scenario() -> None:
        assert await repo.upsert(item) == UpsertResult.INSERTED
        assert await repo.upsert(item) == UpsertResult.UNCHANGED
        assert len(repo.records) == 1

    asyncio.run(scenario())
