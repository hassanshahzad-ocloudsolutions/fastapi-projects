"""adding address id as foreign key in users

Revision ID: 706349ec35cd
Revises: 5d49ccc82db9
Create Date: 2025-11-05 15:16:10.253019

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '706349ec35cd'
down_revision: Union[str, Sequence[str], None] = '5d49ccc82db9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('address_id', sa.Integer(), nullable=True))
    op.create_foreign_key('address_users_foreign_key', source_table='users', referent_table='address',
                           local_cols=['address_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('address_users_foreign_key', table_name='users')
    op.drop_column('users', 'address_id')
