"""Creating first tables

Revision ID: ec8e5a7eeb19
Revises:
Create Date: 2022-02-13 10:40:11.868546

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "ec8e5a7eeb19"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at", sa.TIMESTAMP(), nullable=True, server_default=sa.func.now()
        ),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("short_description", sa.String(), nullable=True),
        sa.Column("long_bio", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username", name="username_unique"),
    )
    op.create_table(
        "liked_post",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at", sa.TIMESTAMP(), nullable=True, server_default=sa.func.now()
        ),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "post_id", name="user_post_unique"),
    )
    op.create_index("liked_post_user_id_idx", "liked_post", ["user_id"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("liked_post_user_id_idx", table_name="liked_post")
    op.drop_table("liked_post")
    op.drop_table("user")
    # ### end Alembic commands ###
