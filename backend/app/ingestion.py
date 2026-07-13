from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import NGO, Opportunity, OpportunityMatch
from app.schemas import OpportunityIngest, OpportunityMatchIn


def upsert_opportunity(db: Session, payload: OpportunityIngest) -> tuple[Opportunity, bool]:
    """Insert or update one global opportunity by deterministic crawler hash."""

    opportunity = db.scalar(
        select(Opportunity).where(Opportunity.normalized_hash == payload.normalized_hash)
    )
    values = payload.model_dump()
    values["official_source_url"] = str(values["official_source_url"])
    created = opportunity is None
    if opportunity is None:
        opportunity = Opportunity(**values)
        db.add(opportunity)
    else:
        for key, value in values.items():
            setattr(opportunity, key, value)
    db.commit()
    db.refresh(opportunity)
    return opportunity, created


def store_match_result(db: Session, payload: OpportunityMatchIn) -> OpportunityMatch:
    """Persist an auditable draft match; approval remains a separate human action."""

    if db.get(NGO, payload.tenant_id) is None or db.get(Opportunity, payload.opportunity_id) is None:
        raise ValueError("tenant and opportunity must exist")
    match = db.scalar(
        select(OpportunityMatch).where(
            OpportunityMatch.tenant_id == payload.tenant_id,
            OpportunityMatch.opportunity_id == payload.opportunity_id,
        )
    )
    values = payload.model_dump()
    if match is None:
        match = OpportunityMatch(**values, review_status="draft")
        db.add(match)
    else:
        for key, value in values.items():
            setattr(match, key, value)
        match.review_status = "draft"
    db.commit()
    db.refresh(match)
    return match
