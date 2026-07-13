import pytest
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.identity import opportunity_source_key
from app.ingestion import upsert_opportunity
from app.models import Opportunity, OpportunityObservation
from app.schemas import OpportunityIngest


def payload(description: str = "Synthetic description") -> OpportunityIngest:
    source_identifier = "SYNTHETIC-OPPORTUNITY-1"
    source_url = "https://example.org/grants/synthetic"
    return OpportunityIngest(
        source_identifier=source_identifier,
        source_key=opportunity_source_key(source_identifier, source_url),
        content_hash=("b" if description == "Synthetic description" else "c") * 64,
        title="Synthetic official opportunity",
        funder="Synthetic public authority",
        description=description,
        eligibility=["Registered Romanian nonprofit"],
        official_source_url=source_url,
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
    assert observations[1].provenance["approval_id"] == "SYNTHETIC-001"
    assert observations[0].content_hash != observations[1].content_hash
    assert observations[0].content_snapshot["description"] == "Synthetic description"
    assert observations[1].content_snapshot["description"] == "Updated synthetic description"


def test_opportunity_rejects_mismatched_source_key(db_session: Session) -> None:
    unsafe = payload().model_copy(update={"source_key": "f" * 64})
    with pytest.raises(ValueError, match="source_key does not match"):
        upsert_opportunity(db_session, unsafe)


def test_valid_different_source_identity_does_not_merge(db_session: Session) -> None:
    first, _ = upsert_opportunity(db_session, payload())
    other_identifier = "SYNTHETIC-OPPORTUNITY-2"
    other_url = "https://example.org/grants/other-synthetic"
    other = OpportunityIngest.model_validate(
        payload().model_dump()
        | {
            "source_identifier": other_identifier,
            "official_source_url": other_url,
            "source_key": opportunity_source_key(other_identifier, other_url),
        }
    )

    second, created = upsert_opportunity(db_session, other)

    assert created is True
    assert second.id != first.id
    assert db_session.query(Opportunity).count() == 2


def test_opportunity_rejects_timezone_naive_observed_at() -> None:
    with pytest.raises(ValidationError, match="observed_at must include a UTC offset"):
        OpportunityIngest.model_validate(
            payload().model_dump() | {"observed_at": "2026-07-13T00:00:00"}
        )
