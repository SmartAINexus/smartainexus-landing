from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from ai.backend_adapter import as_backend_match_payload
from ai.contracts import EvidenceState, MatchFactor, MatchResult
from app.db import Base
from app.ingestion import store_match_result, upsert_opportunity
from app.models import NGO
from app.schemas import OpportunityIngest, OpportunityMatchIn
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


def test_synthetic_ai_match_round_trips_into_auditable_backend_store() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        ngo = NGO(
            official_name="Synthetic NGO",
            registration_number="SYN-E2E-1",
            country_code="RO",
            contact_email="synthetic@example.org",
        )
        session.add(ngo)
        session.commit()
        opportunity, _ = upsert_opportunity(
            session,
            OpportunityIngest(
                normalized_hash="c" * 64,
                title="Synthetic E2E opportunity",
                funder="Synthetic authority",
                description="Synthetic description",
                eligibility=["Romanian nonprofit"],
                official_source_url="https://example.org/e2e-opportunity",
                timezone="Europe/Bucharest",
                provenance={"official_source": True},
            ),
        )
        result = MatchResult(
            score=81,
            factors=(
                MatchFactor(
                    name="geography",
                    score=100,
                    rationale="Synthetic verified geography",
                    evidence_state=EvidenceState.VERIFIED,
                ),
            ),
            requires_human_review=True,
        )
        payload = OpportunityMatchIn.model_validate(
            as_backend_match_payload(
                result,
                tenant_id=str(ngo.id),
                opportunity_id=str(opportunity.id),
                model_provider="synthetic-provider",
                model_id="synthetic-model",
                prompt_version="match-v1",
            )
        )
        stored = store_match_result(session, payload)

    assert stored.score == 81
    assert stored.factors[0]["evidence_state"] == "verified"
    assert stored.review_status == "draft"
