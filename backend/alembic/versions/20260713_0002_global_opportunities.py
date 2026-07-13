"""Create global official-source opportunities."""

from alembic import op
import sqlalchemy as sa

revision = "20260713_0002"
down_revision = "20260713_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "opportunities",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("source_identifier", sa.String(240), nullable=False),
        sa.Column("source_key", sa.String(64), nullable=False),
        sa.Column("content_hash", sa.String(64), nullable=False),
        sa.Column("title", sa.String(240), nullable=False),
        sa.Column("funder", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("eligibility", sa.JSON(), nullable=False),
        sa.Column("official_source_url", sa.String(2048), nullable=False),
        sa.Column("deadline", sa.DateTime(timezone=True), nullable=True),
        sa.Column("timezone", sa.String(64), nullable=False),
        sa.Column("provenance", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_opportunities_source_key",
        "opportunities",
        ["source_key"],
        unique=True,
    )
    op.create_table(
        "opportunity_observations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("opportunity_id", sa.Uuid(), nullable=False),
        sa.Column("content_hash", sa.String(64), nullable=False),
        sa.Column("observed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("provenance", sa.JSON(), nullable=False),
        sa.Column("content_snapshot", sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(["opportunity_id"], ["opportunities.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "opportunity_id", "content_hash", "observed_at", name="uq_observation_version_time"
        ),
    )
    op.create_index(
        "ix_opportunity_observations_opportunity_id",
        "opportunity_observations",
        ["opportunity_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_opportunity_observations_opportunity_id", table_name="opportunity_observations")
    op.drop_table("opportunity_observations")
    op.drop_index("ix_opportunities_source_key", table_name="opportunities")
    op.drop_table("opportunities")
