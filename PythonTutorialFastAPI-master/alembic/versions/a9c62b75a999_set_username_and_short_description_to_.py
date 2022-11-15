"""Set username and short description to not nullable

Revision ID: a9c62b75a999
Revises: ec8e5a7eeb19
Create Date: 2022-02-13 10:49:56.431287

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "a9c62b75a999"
down_revision = "ec8e5a7eeb19"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("user", "username", nullable=False)
    op.alter_column("user", "short_description", nullable=False)
    # op.add_column("user", sa.Column("test", sa.String()))


def downgrade():
    op.drop_column("user", "test")
    op.alter_column("user", "short_description", nullable=True)
    # op.alter_column("user", "username", nullable=True)
