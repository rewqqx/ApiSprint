from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.models.base import Base
from sqlalchemy.sql import func


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    created_by = Column(Integer, ForeignKey('users.id'), index=True)
    modified_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    modified_by = Column(Integer, ForeignKey('users.id'), index=True)

    user_created_by = relationship('User', foreign_keys=[created_by])
    user_modified_by = relationship('User', foreign_keys=[modified_by])
