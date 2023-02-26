from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Computed
from src.models.base import Base
from sqlalchemy.sql import func
from sqlalchemy.inspection import inspect
from alembic import op
import os


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password_hashed = Column(String)
    role = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    created_by = Column(Integer)
    modified_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    modified_by = Column(Integer)
    #
    # op.bulk_insert('users',
    #                [
    #                    {
    #                        'username': os.environ.get('ADMIN_NAME'),
    #                        'password_hashed': os.environ.get('ADMIN_PASSWORD'),
    #                        'role': 'admin'
    #                    }
    #                ])



