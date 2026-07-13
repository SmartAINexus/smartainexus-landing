from sqlalchemy.orm import Session

from app.ingestion import upsert_opportunity
from app.models import OpportunityObservation
from app.schemas import OpportunityIngest


def payload(description: str = "Synthetic description") -> OpportunityIngest:
    return OpportunityIngest(
        source_identifier="SYNTHETIC-OPPORTUNITY-1",
        source_key="a" * 64,
        content_hash=("b" if description == "Synthetic description" else "c") * 64,
        title="Synthetic official opportunity",
        funder="Synthetic public authority",
        description=description,
        eligibility=["Registered Romanian nonprofit"],
        official_source_url="https://example.org/grants/synthetic",
        deadline="2026-09-30T17:00:00+03:00",
        timezone="Europe/Bucharest",
        provenance={"official_source": True, "approval_id": "SYNTHETIC-001"},
        observed_at=(
            "2026-07-13T00:00:00+00:00"
            if description == "Synthetic description"
            else "2026-07-13T01:00:00+00:00"
        ),
    )


def test_opportunity_upsert_is_global_and_hash_deduplicated(db_session: Session) -> None:
    first, created = upsert_opportunity(db_session, payload())
    second, created_again = upsert_opportunity(db_session, payload("Updated synthetic description"))

    assert created is True
    assert created_again is False
    assert first.id == second.id
    assert second.description == "Updated synthetic description"
    observations = db_session.query(OpportunityObservation).order_by(
        OpportunityObservation.observed_at
    ).all()
    assert len(observations) == 2
    assert observations[0].provenance["approval_id"] == "SYNTHETIC-001"
    assert observations[0].content_hash != observations[1].content_hash
