"""Create NGO tenants and grants."""
from alembic import op
import sqlalchemy as sa

revision = "20260713_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "ngos",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("official_name", sa.String(200), nullable=False),
        sa.Column("registration_number", sa.String(80), nullable=False),
        sa.Column("country_code", sa.String(2), nullable=False),
        sa.Column("contact_email", sa.String(320), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("country_code", "registration_number", name="uq_ngo_registration_country"),
    )
    op.create_table(
        "grants",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(240), nullable=False),
        sa.Column("funder", sa.String(200), nullable=False),
        sa.Column("official_source_url", sa.String(2048), nullable=False),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("deadline", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["ngos.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_grants_tenant_id", "grants", ["tenant_id"])


def downgrade() -> None:
    op.drop_index("ix_grants_tenant_id", table_name="grants")
    op.drop_table("grants")
    op.drop_table("ngos")

