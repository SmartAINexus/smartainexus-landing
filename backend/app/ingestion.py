import hmac

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.identity import opportunity_source_key
from app.models import NGO, Opportunity, OpportunityMatch, OpportunityObservation
from app.schemas import OpportunityIngest, OpportunityMatchIn


def _is_expected_unique_violation(
    error: IntegrityError, *, postgres_constraint: str, sqlite_columns: str
) -> bool:
    diagnostic = getattr(error.orig, "diag", None)
    constraint_name = getattr(diagnostic, "constraint_name", None)
    if constraint_name is not None:
        return constraint_name == postgres_constraint
    return f"UNIQUE constraint failed: {sqlite_columns}" in str(error.orig)


def upsert_opportunity(db: Session, payload: OpportunityIngest) -> tuple[Opportunity, bool]:
    """Insert or update one global opportunity by deterministic crawler hash."""

    expected_key = opportunity_source_key(
        payload.source_identifier, str(payload.official_source_url)
    )
    if not hmac.compare_digest(payload.source_key, expected_key):
        raise ValueError("source_key does not match source identifier and URL")
    opportunity = db.scalar(
        select(Opportunity).where(Opportunity.source_key == payload.source_key)
    )
    content_snapshot = payload.model_dump(
        mode="json", exclude={"provenance", "observed_at"}
    )
    values = payload.model_dump()
    observed_at = values.pop("observed_at")
    provenance = values.pop("provenance")
    values["official_source_url"] = str(values["official_source_url"])
    created = False
    if opportunity is None:
        candidate = Opportunity(**values, provenance=provenance)
        try:
            with db.begin_nested():
                db.add(candidate)
                db.flush()
            opportunity = candidate
            created = True
        except IntegrityError as error:
            if not _is_expected_unique_violation(
                error,
                postgres_constraint="ix_opportunities_source_key",
                sqlite_columns="opportunities.source_key",
            ):
                raise
            opportunity = db.scalar(
                select(Opportunity).where(Opportunity.source_key == payload.source_key)
            )
            if opportunity is None:
                raise

    if not created:
        if (
            opportunity.source_identifier != payload.source_identifier
            or opportunity.official_source_url != str(payload.official_source_url)
        ):
            raise ValueError("source identity fields cannot change for an existing source_key")
    db.flush()
    observation = db.scalar(
        select(OpportunityObservation).where(
            OpportunityObservation.opportunity_id == opportunity.id,
            OpportunityObservation.content_hash == payload.content_hash,
            OpportunityObservation.observed_at == observed_at,
        )
    )
    if observation is None:
        try:
            with db.begin_nested():
                db.add(
                    OpportunityObservation(
                        opportunity_id=opportunity.id,
                        content_hash=payload.content_hash,
                        observed_at=observed_at,
                        provenance=provenance,
                        content_snapshot=content_snapshot,
                    )
                )
                db.flush()
        except IntegrityError as error:
            if not _is_expected_unique_violation(
                error,
                postgres_constraint="uq_observation_version_time",
                sqlite_columns=(
                    "opportunity_observations.opportunity_id, "
                    "opportunity_observations.content_hash, "
                    "opportunity_observations.observed_at"
                ),
            ):
                raise
            observation = db.scalar(
                select(OpportunityObservation).where(
                    OpportunityObservation.opportunity_id == opportunity.id,
                    OpportunityObservation.content_hash == payload.content_hash,
                    OpportunityObservation.observed_at == observed_at,
                )
            )
            if observation is None:
                raise
            if (
                observation.provenance != provenance
                or observation.content_snapshot != content_snapshot
            ):
                raise ValueError("observation identity conflicts with retained evidence")
    if not created:
        for key, value in values.items():
            setattr(opportunity, key, value)
        opportunity.provenance = provenance
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
