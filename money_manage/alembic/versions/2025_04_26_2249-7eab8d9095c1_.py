"""empty message

Revision ID: 7eab8d9095c1
Revises: b350da87a217
Create Date: 2025-04-26 22:49:34.557800

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7eab8d9095c1"
down_revision: Union[str, None] = "b350da87a217"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "categories",
        sa.Column("name", sa.String(length=256), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "currencies",
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=32), nullable=False),
        sa.Column("exchange_rate", sa.DECIMAL(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "transactions_type",
        sa.Column("eng_name", sa.String(length=128), nullable=False),
        sa.Column("ru_name", sa.String(length=128), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "transactions",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("description", sa.String(length=256), nullable=True),
        sa.Column("amount", sa.DECIMAL(), nullable=False),
        sa.Column("transaction_type_id", sa.Integer(), nullable=False),
        sa.Column("currency_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.CheckConstraint(
            "amount >= 0 AND amount <= 999999999999",
            name="check_amount_positive",
        ),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["categories.id"],
        ),
        sa.ForeignKeyConstraint(
            ["currency_id"],
            ["currencies.id"],
        ),
        sa.ForeignKeyConstraint(
            ["transaction_type_id"],
            ["transactions_type.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("transactions")
    op.drop_table("transactions_type")
    op.drop_table("currencies")
    op.drop_table("categories")
    # ### end Alembic commands ###
