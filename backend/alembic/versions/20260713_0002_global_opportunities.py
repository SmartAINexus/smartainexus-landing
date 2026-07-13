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
        sa.Column("normalized_hash", sa.String(64), nullable=False),
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
        "ix_opportunities_normalized_hash",
        "opportunities",
        ["normalized_hash"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("ix_opportunities_normalized_hash", table_name="opportunities")
    op.drop_table("opportunities")
