"""empty message

Revision ID: 71c20dc61d5d
Revises: d2b8ca9bb7f1
Create Date: 2025-12-04 16:43:39.223926

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '71c20dc61d5d'
down_revision: Union[str, Sequence[str], None] = 'd2b8ca9bb7f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE SCHEMA IF NOT EXISTS celery;")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP SCHEMA IF EXISTS celery;")
