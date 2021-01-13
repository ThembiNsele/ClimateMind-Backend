"""CM-334 - task CM-359 - add climate_feed table

Revision ID: 713ba83ef1ed
Revises: d10c6bfdd9aa
Create Date: 2021-01-11 12:33:39.636545

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = "713ba83ef1ed"
down_revision = "d10c6bfdd9aa"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "climate_feed",
        sa.Column("climate_feed_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("session_id", sa.String(length=256), nullable=True),
        sa.Column("event_ts", sa.DateTime(), nullable=True),
        sa.Column("effect_position", sa.Integer(), nullable=True),
        sa.Column("effect_iri", sa.String(length=255), nullable=True),
        sa.Column("effect_score", sa.Float(), nullable=True),
        sa.Column("solution_1_iri", sa.String(length=255), nullable=True),
        sa.Column("solution_2_iri", sa.String(length=255), nullable=True),
        sa.Column("solution_3_iri", sa.String(length=255), nullable=True),
        sa.Column("solution_4_iri", sa.String(length=255), nullable=True),
        sa.Column("isPossiblyLocal", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["sessions.session_id"],
        ),
        sa.PrimaryKeyConstraint("climate_feed_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("climate_feed")
    # ### end Alembic commands ###
