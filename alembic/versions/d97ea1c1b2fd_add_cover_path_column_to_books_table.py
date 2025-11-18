"""add cover_path column to books table

Revision ID: d97ea1c1b2fd
Revises: a9ea6d4aa1f3
Create Date: 2025-11-18 21:39:22.743750

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd97ea1c1b2fd'
down_revision: Union[str, Sequence[str], None] = 'a9ea6d4aa1f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add cover_path column to books table"""
    op.add_column('books', sa.Column('cover_path', sa.String(300), nullable=True))


def downgrade() -> None:
    """Remove cover_path column from books table"""
    op.drop_column('books', 'cover_path')
