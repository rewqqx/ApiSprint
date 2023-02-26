from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from src.models.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Tank(Base):
    __tablename__ = 'tanks'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    max_capacity = Column(Float)
    current_capacity = Column(Float)
    product_id = Column(Integer, ForeignKey('products.id'), index=True)
    created_at = Column(DateTime, server_default=func.now())
    created_by = Column(Integer, ForeignKey('users.id'))
    modified_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    modified_by = Column(Integer, ForeignKey('users.id'))

    product = relationship('Product', foreign_keys=[product_id])
    user_created_by = relationship('User', foreign_keys=[created_by])
    user_modified_by = relationship('User', foreign_keys=[modified_by])

