import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, DateTime, ForeignKey, Index, String, Text, UniqueConstraint
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
