"""CM-791 delete postal codes from sessions, specify what the uuid is for in each table

Revision ID: 86dbb3c839d6
Revises: ff1d6f5eb900
Create Date: 2021-08-29 16:35:43.618525

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = "86dbb3c839d6"
down_revision = "ff1d6f5eb900"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("sessions", "postal_code")
    op.alter_column("users", "uuid", new_column_name="user_uuid")
    op.alter_column("users", "email", new_column_name="user_email")
    op.alter_column("signup", "email", new_column_name="signup_email")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "sessions",
        sa.Column(
            "postal_code",
            sa.VARCHAR(length=5, collation="SQL_Latin1_General_CP1_CI_AS"),
            autoincrement=False,
            nullable=True,
        ),
    )
    # ### end Alembic commands ###
