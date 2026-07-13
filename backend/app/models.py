import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    JSON,
    CheckConstraint,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class GrantStatus(str, enum.Enum):
    identified = "identified"
    reviewing = "reviewing"
    selected = "selected"
    archived = "archived"


class NGO(Base):
    __tablename__ = "ngos"
    __table_args__ = (
        UniqueConstraint("country_code", "registration_number", name="uq_ngo_registration_country"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    official_name: Mapped[str] = mapped_column(String(200))
    registration_number: Mapped[str] = mapped_column(String(80))
    country_code: Mapped[str] = mapped_column(String(2))
    contact_email: Mapped[str] = mapped_column(String(320))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    grants: Mapped[list["Grant"]] = relationship(back_populates="ngo", cascade="all, delete-orphan")


class Grant(Base):
    __tablename__ = "grants"
    __table_args__ = (Index("ix_grants_tenant_id", "tenant_id"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ngos.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(240))
    funder: Mapped[str] = mapped_column(String(200))
    official_source_url: Mapped[str] = mapped_column(String(2048))
    status: Mapped[str] = mapped_column(String(32), default=GrantStatus.identified.value)
    deadline: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    ngo: Mapped[NGO] = relationship(back_populates="grants")


class Opportunity(Base):
    """Global official-source opportunity, independent from any NGO tenant."""

    __tablename__ = "opportunities"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    normalized_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(240))
    funder: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    eligibility: Mapped[list[str]] = mapped_column(JSON)
    official_source_url: Mapped[str] = mapped_column(String(2048))
    deadline: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    timezone: Mapped[str] = mapped_column(String(64))
    provenance: Mapped[dict[str, object]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )


class OpportunityMatch(Base):
    """Tenant-scoped, reviewable assessment of one global opportunity."""

    __tablename__ = "opportunity_matches"
    __table_args__ = (
        Index("ix_opportunity_matches_tenant_id", "tenant_id"),
        Index("ix_opportunity_matches_tenant_opportunity", "tenant_id", "opportunity_id"),
        UniqueConstraint(
            "tenant_id", "opportunity_id", "version", name="uq_match_tenant_opportunity_version"
        ),
        UniqueConstraint(
            "id", "tenant_id", "opportunity_id", name="uq_match_lineage_target"
        ),
        ForeignKeyConstraint(
            ["supersedes_id", "tenant_id", "opportunity_id"],
            [
                "opportunity_matches.id",
                "opportunity_matches.tenant_id",
                "opportunity_matches.opportunity_id",
            ],
            name="fk_match_supersedes_same_scope",
            ondelete="RESTRICT",
        ),
        CheckConstraint("score >= 0 AND score <= 100", name="ck_match_score_range"),
        CheckConstraint("requires_human_review = true", name="ck_match_human_review_required"),
        CheckConstraint("review_status IN ('draft', 'reviewed', 'rejected')", name="ck_match_review_status"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ngos.id", ondelete="CASCADE"))
    opportunity_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("opportunities.id", ondelete="CASCADE")
    )
    supersedes_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    version: Mapped[int] = mapped_column()
    score: Mapped[int] = mapped_column()
    factors: Mapped[list[dict[str, object]]] = mapped_column(JSON)
    missing_information: Mapped[list[str]] = mapped_column(JSON)
    exclusion_risks: Mapped[list[str]] = mapped_column(JSON)
    requires_human_review: Mapped[bool] = mapped_column(default=True)
    review_status: Mapped[str] = mapped_column(String(32), default="draft")
    model_provider: Mapped[str] = mapped_column(String(80))
    model_id: Mapped[str] = mapped_column(String(120))
    prompt_version: Mapped[str] = mapped_column(String(40))
    calculated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
