"""upd

Revision ID: b5a7356bcb91
Revises: fe59eb9df90b
Create Date: 2023-02-24 19:35:24.330842

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b5a7356bcb91'
down_revision = 'fe59eb9df90b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('operations_created_by_fkey', 'operations', type_='foreignkey')
    op.drop_constraint('operations_modified_by_fkey', 'operations', type_='foreignkey')
    op.create_foreign_key(None, 'operations', 'users', ['modified_by'], ['id'])
    op.create_foreign_key(None, 'operations', 'users', ['created_by'], ['id'])
    op.drop_constraint('products_created_by_fkey', 'products', type_='foreignkey')
    op.drop_constraint('products_modified_by_fkey', 'products', type_='foreignkey')
    op.create_foreign_key(None, 'products', 'users', ['modified_by'], ['id'])
    op.create_foreign_key(None, 'products', 'users', ['created_by'], ['id'])
    op.drop_constraint('tanks_created_by_fkey', 'tanks', type_='foreignkey')
    op.drop_constraint('tanks_modified_by_fkey', 'tanks', type_='foreignkey')
    op.create_foreign_key(None, 'tanks', 'users', ['modified_by'], ['id'])
    op.create_foreign_key(None, 'tanks', 'users', ['created_by'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tanks', type_='foreignkey')
    op.drop_constraint(None, 'tanks', type_='foreignkey')
    op.create_foreign_key('tanks_modified_by_fkey', 'tanks', 'users', ['modified_by'], ['id'], onupdate='CASCADE', ondelete='RESTRICT')
    op.create_foreign_key('tanks_created_by_fkey', 'tanks', 'users', ['created_by'], ['id'], onupdate='CASCADE', ondelete='RESTRICT')
    op.drop_constraint(None, 'products', type_='foreignkey')
    op.drop_constraint(None, 'products', type_='foreignkey')
    op.create_foreign_key('products_modified_by_fkey', 'products', 'users', ['modified_by'], ['id'], onupdate='CASCADE', ondelete='RESTRICT')
    op.create_foreign_key('products_created_by_fkey', 'products', 'users', ['created_by'], ['id'], onupdate='CASCADE', ondelete='RESTRICT')
    op.drop_constraint(None, 'operations', type_='foreignkey')
    op.drop_constraint(None, 'operations', type_='foreignkey')
    op.create_foreign_key('operations_modified_by_fkey', 'operations', 'users', ['modified_by'], ['id'], onupdate='CASCADE', ondelete='RESTRICT')
    op.create_foreign_key('operations_created_by_fkey', 'operations', 'users', ['created_by'], ['id'], onupdate='CASCADE', ondelete='RESTRICT')
    # ### end Alembic commands ###
