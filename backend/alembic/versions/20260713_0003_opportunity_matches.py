"""Create tenant-scoped opportunity matches."""

from alembic import op
import sqlalchemy as sa

revision = "20260713_0003"
down_revision = "20260713_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "opportunity_matches",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("opportunity_id", sa.Uuid(), nullable=False),
        sa.Column("supersedes_id", sa.Uuid(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("factors", sa.JSON(), nullable=False),
        sa.Column("missing_information", sa.JSON(), nullable=False),
        sa.Column("exclusion_risks", sa.JSON(), nullable=False),
        sa.Column("requires_human_review", sa.Boolean(), nullable=False),
        sa.Column("review_status", sa.String(32), nullable=False),
        sa.Column("model_provider", sa.String(80), nullable=False),
        sa.Column("model_id", sa.String(120), nullable=False),
        sa.Column("prompt_version", sa.String(40), nullable=False),
        sa.Column("calculated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["ngos.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["opportunity_id"], ["opportunities.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["supersedes_id", "tenant_id", "opportunity_id"],
            [
                "opportunity_matches.id",
                "opportunity_matches.tenant_id",
                "opportunity_matches.opportunity_id",
            ],
            name="fk_match_supersedes_same_scope",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "tenant_id", "opportunity_id", "version", name="uq_match_tenant_opportunity_version"
        ),
        sa.UniqueConstraint("id", "tenant_id", "opportunity_id", name="uq_match_lineage_target"),
        sa.CheckConstraint("score >= 0 AND score <= 100", name="ck_match_score_range"),
        sa.CheckConstraint("requires_human_review = true", name="ck_match_human_review_required"),
        sa.CheckConstraint(
            "review_status IN ('draft', 'reviewed', 'rejected')", name="ck_match_review_status"
        ),
    )
    op.create_index(
        "ix_opportunity_matches_tenant_id", "opportunity_matches", ["tenant_id"]
    )
    op.create_index(
        "ix_opportunity_matches_tenant_opportunity",
        "opportunity_matches",
        ["tenant_id", "opportunity_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_opportunity_matches_tenant_opportunity", table_name="opportunity_matches")
    op.drop_index("ix_opportunity_matches_tenant_id", table_name="opportunity_matches")
    op.drop_table("opportunity_matches")
