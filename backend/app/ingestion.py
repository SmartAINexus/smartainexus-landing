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
    """Append an auditable draft match; prior calculations are never overwritten."""

    if db.get(NGO, payload.tenant_id) is None or db.get(Opportunity, payload.opportunity_id) is None:
        raise ValueError("tenant and opportunity must exist")
    previous = db.scalar(
        select(OpportunityMatch).where(
            OpportunityMatch.tenant_id == payload.tenant_id,
            OpportunityMatch.opportunity_id == payload.opportunity_id,
        ).order_by(OpportunityMatch.version.desc()).with_for_update()
    )
    values = payload.model_dump()
    values["requires_human_review"] = True
    match = OpportunityMatch(
        **values,
        review_status="draft",
        supersedes_id=previous.id if previous else None,
        version=(previous.version + 1) if previous else 1,
    )
    db.add(match)
    db.commit()
    db.refresh(match)
    return match
