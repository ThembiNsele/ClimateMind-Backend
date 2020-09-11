"""added LRF table

Revision ID: f2aa428afb8c
Revises: e19c2ec43c46
Create Date: 2020-09-11 13:30:54.133543

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2aa428afb8c'
down_revision = 'e19c2ec43c46'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('LRF',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('iri', sa.String(length=120), nullable=True),
    sa.Column('zip', sa.Integer(), nullable=True),
    sa.Column('affected_by_iri', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_LRF_zip'), 'LRF', ['zip'], unique=False)
    op.add_column('user', sa.Column('zip', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'zip')
    op.drop_index(op.f('ix_LRF_zip'), table_name='LRF')
    op.drop_table('LRF')
    # ### end Alembic commands ###
