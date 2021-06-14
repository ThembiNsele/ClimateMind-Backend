"""CM-736 add all current tables

Revision ID: 1382a124cd8e
Revises: 
Create Date: 2021-06-10 19:30:51.458170

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = "1382a124cd8e"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "analytics_data",
        sa.Column("analytics_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("category", sa.String(length=50), nullable=True),
        sa.Column("action", sa.String(length=50), nullable=True),
        sa.Column("label", sa.String(length=50), nullable=True),
        sa.Column("session_uuid", mssql.UNIQUEIDENTIFIER(), nullable=True),
        sa.Column("event_timestamp", sa.DateTime(), nullable=True),
        sa.Column("value", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("analytics_id"),
    )
    op.create_table(
        "sessions",
        sa.Column("postal_code", sa.String(length=5), nullable=True),
        sa.Column("ip_address", sa.String(length=255), nullable=True),
        sa.Column("session_uuid", mssql.UNIQUEIDENTIFIER(), nullable=False),
        sa.PrimaryKeyConstraint("session_uuid"),
    )
    op.create_table(
        "users",
        sa.Column("uuid", mssql.UNIQUEIDENTIFIER(), nullable=False),
        sa.Column("email", sa.String(length=120), nullable=True),
        sa.Column("full_name", sa.String(length=50), nullable=False),
        sa.Column("user_created_timestamp", sa.DateTime(), nullable=True),
        sa.Column("password_hash", sa.String(length=128), nullable=True),
        sa.PrimaryKeyConstraint("uuid"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_table(
        "climate_feed",
        sa.Column("climate_feed_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("event_timestamp", sa.DateTime(), nullable=True),
        sa.Column("effect_position", sa.Integer(), nullable=True),
        sa.Column("effect_iri", sa.String(length=255), nullable=True),
        sa.Column("effect_score", sa.Float(), nullable=True),
        sa.Column("solution_1_iri", sa.String(length=255), nullable=True),
        sa.Column("solution_2_iri", sa.String(length=255), nullable=True),
        sa.Column("solution_3_iri", sa.String(length=255), nullable=True),
        sa.Column("solution_4_iri", sa.String(length=255), nullable=True),
        sa.Column("isPossiblyLocal", sa.Boolean(), nullable=True),
        sa.Column("session_uuid", mssql.UNIQUEIDENTIFIER(), nullable=True),
        sa.ForeignKeyConstraint(
            ["session_uuid"],
            ["sessions.session_uuid"],
        ),
        sa.PrimaryKeyConstraint("climate_feed_id"),
    )
    op.create_table(
        "scores",
        sa.Column("scores_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("security", sa.Float(), nullable=True),
        sa.Column("conformity", sa.Float(), nullable=True),
        sa.Column("benevolence", sa.Float(), nullable=True),
        sa.Column("tradition", sa.Float(), nullable=True),
        sa.Column("universalism", sa.Float(), nullable=True),
        sa.Column("self_direction", sa.Float(), nullable=True),
        sa.Column("stimulation", sa.Float(), nullable=True),
        sa.Column("hedonism", sa.Float(), nullable=True),
        sa.Column("achievement", sa.Float(), nullable=True),
        sa.Column("power", sa.Float(), nullable=True),
        sa.Column("user_uuid", mssql.UNIQUEIDENTIFIER(), nullable=True),
        sa.Column("scores_created_timestamp", sa.DateTime(), nullable=True),
        sa.Column("session_uuid", mssql.UNIQUEIDENTIFIER(), nullable=True),
        sa.ForeignKeyConstraint(
            ["session_uuid"],
            ["sessions.session_uuid"],
        ),
        sa.ForeignKeyConstraint(
            ["user_uuid"],
            ["users.uuid"],
        ),
        sa.PrimaryKeyConstraint("scores_id"),
    )
    op.create_table(
        "signup",
        sa.Column("email", sa.String(length=254), nullable=True),
        sa.Column("signup_timestamp", sa.DateTime(), nullable=True),
        sa.Column("session_uuid", mssql.UNIQUEIDENTIFIER(), nullable=True),
        sa.Column("signup_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(
            ["session_uuid"],
            ["sessions.session_uuid"],
        ),
        sa.PrimaryKeyConstraint("signup_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("signup")
    op.drop_table("scores")
    op.drop_table("climate_feed")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    op.drop_table("sessions")
    op.drop_table("analytics_data")
    # ### end Alembic commands ###
