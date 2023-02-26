"""upd1

Revision ID: ef78d752e3cd
Revises: c0a40a5fb786
Create Date: 2023-02-26 15:03:34.183528

"""
from alembic import op
import sqlalchemy as sa
import os


# revision identifiers, used by Alembic.
revision = 'ef78d752e3cd'
down_revision = 'c0a40a5fb786'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # get metadata from current connection
    meta = sa.MetaData()

    # pass in tuple with tables we want to reflect, otherwise whole database will get reflected
    meta.reflect(only=('users',), bind=op.get_bind())

    # define table representation
    some_table_tbl = sa.Table('users', meta)

    # insert records
    op.bulk_insert(
        some_table_tbl,
        [
            {
                           'username': os.environ.get('ADMIN_NAME'),
                           'password_hashed': os.environ.get('ADMIN_PASSWORD'),
                           'role': 'admin'
                       },
        ]
    )

def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###