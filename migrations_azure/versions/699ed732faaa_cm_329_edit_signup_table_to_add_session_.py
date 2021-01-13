"""CM-329 edit signup table to add session_id column

Revision ID: 699ed732faaa
Revises: 713ba83ef1ed
Create Date: 2021-01-13 19:10:50.304365

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = "699ed732faaa"
down_revision = "713ba83ef1ed"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "signup", sa.Column("session_id", sa.String(length=256), nullable=True)
    )
    op.create_foreign_key(None, "signup", "sessions", ["session_id"], ["session_id"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "signup", type_="foreignkey")
    op.drop_column("signup", "session_id")
    # ### end Alembic commands ###
