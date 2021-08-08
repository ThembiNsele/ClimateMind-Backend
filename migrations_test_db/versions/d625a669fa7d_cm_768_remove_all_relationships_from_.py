"""CM-768 remove all relationships from tables

Revision ID: d625a669fa7d
Revises: 1a9369559ca2
Create Date: 2021-07-14 19:33:20.299394

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d625a669fa7d"
down_revision = "1a9369559ca2"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "FK__climate_f__sessi__3864608B", "climate_feed", type_="foreignkey"
    )
    op.drop_constraint("FK__scores__session___3B40CD36", "scores", type_="foreignkey")
    op.drop_constraint("FK__scores__user_uui__3C34F16F", "scores", type_="foreignkey")
    op.drop_constraint("FK__signup__session___3F115E1A", "signup", type_="foreignkey")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(
        "FK__signup__session___3F115E1A",
        "signup",
        "sessions",
        ["session_uuid"],
        ["session_uuid"],
    )
    op.create_foreign_key(
        "FK__scores__user_uui__3C34F16F", "scores", "users", ["user_uuid"], ["uuid"]
    )
    op.create_foreign_key(
        "FK__scores__session___3B40CD36",
        "scores",
        "sessions",
        ["session_uuid"],
        ["session_uuid"],
    )
    op.create_foreign_key(
        "FK__climate_f__sessi__3864608B",
        "climate_feed",
        "sessions",
        ["session_uuid"],
        ["session_uuid"],
    )
    # ### end Alembic commands ###
