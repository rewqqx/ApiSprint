from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.models.base import Base
from sqlalchemy.sql import func


class Operation(Base):
    __tablename__ = 'operations'
    id = Column(Integer, primary_key=True)
    mass = Column(Float)
    date_start = Column(DateTime)
    date_end = Column(DateTime)
    tank_id = Column(Integer, ForeignKey('tanks.id'), index=True)
    product_id = Column(Integer, ForeignKey('products.id'), index=True)
    created_at = Column(DateTime, server_default=func.now())
    created_by = Column(Integer, ForeignKey('users.id'), index=True)
    modified_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    modified_by = Column(Integer, ForeignKey('users.id'), index=True)

    tank = relationship('Tank', backref='tanks')
    product = relationship('Product', backref='products')

    user_created_by = relationship('User', foreign_keys=[created_by])
    user_modified_by = relationship('User', foreign_keys=[modified_by])
