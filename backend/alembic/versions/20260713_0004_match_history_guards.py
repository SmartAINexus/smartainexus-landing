"""Make opportunity matches append-only and fail-closed."""

from alembic import op
import sqlalchemy as sa

revision = "20260713_0004"
down_revision = "20260713_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_constraint("uq_match_tenant_opportunity", "opportunity_matches", type_="unique")
    op.add_column(
        "opportunity_matches",
        sa.Column("supersedes_id", sa.Uuid(), nullable=True),
    )
    op.create_foreign_key(
        "fk_match_supersedes",
        "opportunity_matches",
        "opportunity_matches",
        ["supersedes_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_index(
        "ix_opportunity_matches_tenant_opportunity",
        "opportunity_matches",
        ["tenant_id", "opportunity_id"],
    )
    op.create_check_constraint(
        "ck_match_score_range", "opportunity_matches", "score >= 0 AND score <= 100"
    )
    op.create_check_constraint(
        "ck_match_human_review_required",
        "opportunity_matches",
        "requires_human_review = true",
    )
    op.create_check_constraint(
        "ck_match_review_status",
        "opportunity_matches",
        "review_status IN ('draft', 'reviewed', 'rejected')",
    )


def downgrade() -> None:
    op.drop_constraint("ck_match_review_status", "opportunity_matches", type_="check")
    op.drop_constraint("ck_match_human_review_required", "opportunity_matches", type_="check")
    op.drop_constraint("ck_match_score_range", "opportunity_matches", type_="check")
    op.drop_index("ix_opportunity_matches_tenant_opportunity", table_name="opportunity_matches")
    op.drop_constraint("fk_match_supersedes", "opportunity_matches", type_="foreignkey")
    op.drop_column("opportunity_matches", "supersedes_id")
    op.create_unique_constraint(
        "uq_match_tenant_opportunity",
        "opportunity_matches",
        ["tenant_id", "opportunity_id"],
    )
