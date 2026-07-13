from sqlalchemy.orm import Session

from app.ingestion import upsert_opportunity
from app.schemas import OpportunityIngest


def payload(description: str = "Synthetic description") -> OpportunityIngest:
    return OpportunityIngest(
        normalized_hash="a" * 64,
        title="Synthetic official opportunity",
        funder="Synthetic public authority",
        description=description,
        eligibility=["Registered Romanian nonprofit"],
        official_source_url="https://example.org/grants/synthetic",
        deadline="2026-09-30T17:00:00+03:00",
        timezone="Europe/Bucharest",
        provenance={"official_source": True, "approval_id": "SYNTHETIC-001"},
    )


def test_opportunity_upsert_is_global_and_hash_deduplicated(db_session: Session) -> None:
    first, created = upsert_opportunity(db_session, payload())
    second, created_again = upsert_opportunity(db_session, payload("Updated synthetic description"))

    assert created is True
    assert created_again is False
    assert first.id == second.id
    assert second.description == "Updated synthetic description"
