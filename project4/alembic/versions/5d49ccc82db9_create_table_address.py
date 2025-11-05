"""create table address

Revision ID: 5d49ccc82db9
Revises: 95aa4679825b
Create Date: 2025-11-05 15:04:50.797099

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d49ccc82db9'
down_revision: Union[str, Sequence[str], None] = '95aa4679825b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table('address', 
                     sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                     sa.Column('address1', sa.String(), nullable=False),
                     sa.Column('address2', sa.String(), nullable=False),
                     sa.Column('city', sa.String(), nullable=False),
                     sa.Column('state', sa.String(), nullable=False),
                     sa.Column('country', sa.String(),nullable=False),
                     sa.Column('postal_code', sa.String(), nullable=False))

def downgrade() -> None:
    op.drop_table('address')
