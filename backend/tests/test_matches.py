import pytest
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.ingestion import store_match_result, upsert_opportunity
from app.models import NGO
from app.schemas import OpportunityIngest, OpportunityMatchIn


def test_match_is_tenant_scoped_auditable_and_always_returns_to_draft(
    db_session: Session,
) -> None:
    ngo = NGO(
        official_name="Synthetic NGO",
        registration_number="SYN-MATCH-1",
        country_code="RO",
        contact_email="synthetic@example.org",
    )
    db_session.add(ngo)
    db_session.commit()
    opportunity, _ = upsert_opportunity(
        db_session,
        OpportunityIngest(
            normalized_hash="b" * 64,
            title="Synthetic opportunity",
            funder="Synthetic authority",
            description="Synthetic description",
            eligibility=["Synthetic eligibility"],
            official_source_url="https://example.org/opportunity",
            timezone="Europe/Bucharest",
            provenance={"official_source": True},
        ),
    )
    payload = OpportunityMatchIn(
        tenant_id=ngo.id,
        opportunity_id=opportunity.id,
        score=72,
        factors=[{"name": "geography", "score": 90, "evidence_state": "verified"}],
        exclusion_risks=["Synthetic legal-form check"],
        requires_human_review=True,
        model_provider="synthetic-test-provider",
        model_id="synthetic-test-model",
        prompt_version="match-v1",
    )

    first = store_match_result(db_session, payload)
    first.review_status = "reviewed"
    db_session.commit()
    updated = store_match_result(db_session, payload.model_copy(update={"score": 74}))

    assert first.id != updated.id
    assert updated.supersedes_id == first.id
    assert updated.score == 74
    assert updated.review_status == "draft"
    assert updated.requires_human_review is True
    assert first.review_status == "reviewed"
    assert first.score == 72


def test_match_input_rejects_disabling_human_review() -> None:
    with pytest.raises(ValidationError):
        OpportunityMatchIn(
            tenant_id="00000000-0000-0000-0000-000000000001",
            opportunity_id="00000000-0000-0000-0000-000000000002",
            score=50,
            requires_human_review=False,
            model_provider="synthetic-provider",
            model_id="synthetic-model",
            prompt_version="match-v1",
        )
