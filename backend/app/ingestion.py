from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Opportunity
from app.schemas import OpportunityIngest


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
