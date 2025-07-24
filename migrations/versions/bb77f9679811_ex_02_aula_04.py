"""exercicio 02 aula 04

Revision ID: bb77f9679811
Revises: 74f39286e2f6
Create Date: 2024-09-06 20:14:23.866062

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb77f9679811'
down_revision: Union[str, None] = '74f39286e2f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:  

        batch_op.add_column(   
            sa.Column(
                'updated_at',
                sa.DateTime(),
                server_default=sa.text('(CURRENT_TIMESTAMP)'),
                nullable=False,
            )
        )


def downgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:  
        batch_op.drop_column('updated_at')
