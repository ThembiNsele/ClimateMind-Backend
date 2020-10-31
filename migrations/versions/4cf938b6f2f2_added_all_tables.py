"""added all tables

Revision ID: 4cf938b6f2f2
Revises: 
Create Date: 2020-10-31 00:19:12.183507

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4cf938b6f2f2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sessions',
    sa.Column('session_id', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('session_id')
    )
    op.create_table('users',
    sa.Column('user_id', sa.String(length=256), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('scores',
    sa.Column('scores_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('session_id', sa.String(length=256), nullable=True),
    sa.Column('security', sa.Float(), nullable=True),
    sa.Column('conformity', sa.Float(), nullable=True),
    sa.Column('benevolence', sa.Float(), nullable=True),
    sa.Column('tradition', sa.Float(), nullable=True),
    sa.Column('universalism', sa.Float(), nullable=True),
    sa.Column('self_direction', sa.Float(), nullable=True),
    sa.Column('stimulation', sa.Float(), nullable=True),
    sa.Column('hedonism', sa.Float(), nullable=True),
    sa.Column('achievement', sa.Float(), nullable=True),
    sa.Column('power', sa.Float(), nullable=True),
    sa.Column('user_id', sa.String(length=256), nullable=True),
    sa.ForeignKeyConstraint(['session_id'], ['sessions.session_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('scores_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('scores')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('sessions')
    # ### end Alembic commands ###
