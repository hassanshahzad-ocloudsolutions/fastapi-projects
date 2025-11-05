"""optional field in address

Revision ID: 944ead113862
Revises: 706349ec35cd
Create Date: 2025-11-05 16:42:19.358038

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '944ead113862'
down_revision: Union[str, Sequence[str], None] = '706349ec35cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('address', sa.Column('apt_num', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('address','apt_num')
