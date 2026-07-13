from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db import Base
from app.ingestion import upsert_opportunity
from app.schemas import OpportunityIngest
from grantbridge_crawler.parser import DataAttributeOpportunityParser
from grantbridge_crawler.policy import SourceApproval


def test_synthetic_crawler_record_round_trips_into_global_backend_store() -> None:
    fixture = (
        Path(__file__).parents[1]
        / "crawler"
        / "tests"
        / "fixtures"
        / "official_opportunities.html"
    )
    approval = SourceApproval(
        host="funding.example.test",
        approval_id="synthetic-integration",
        official_source=True,
        terms_approved=True,
        terms_evidence="synthetic terms approval",
        robots_allowed=True,
        robots_evidence="synthetic robots approval",
    )
    record = DataAttributeOpportunityParser().parse(
        fixture.read_text(encoding="utf-8"),
        source_url="https://funding.example.test/calls",
        retrieved_at=datetime(2026, 7, 13, tzinfo=timezone.utc),
        approval=approval,
    )[0]
    payload = OpportunityIngest.model_validate(record.as_ingest_payload())

    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        first, created = upsert_opportunity(session, payload)
        second, created_again = upsert_opportunity(session, payload)

    assert created is True
    assert created_again is False
    assert first.id == second.id
    assert second.normalized_hash == record.normalized_hash
    assert second.provenance["official_source"] is True
