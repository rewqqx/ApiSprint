from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.models.product import Product
from src.models.schemas.product.product_request import ProductRequest
from src.services.users import get_current_user_id


class ProductsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def all(self) -> List[Product]:
        products = (
            self.session
            .query(Product)
            .order_by(
                Product.id.desc()
            )
            .all()
        )
        return products

    def get(self, product_id: int) -> Product:
        product = (
            self.session
            .query(Product)
            .filter(
                Product.id == product_id,
            )
            .first()
        )
        return product

    def add(self, user_id: int, product_schema: ProductRequest) -> Product:
        product_dict = product_schema.dict()
        print(user_id)
        product_dict['created_by'] = user_id
        product_dict['modified_by'] = user_id
        product = Product(**product_dict)
        self.session.add(product)
        self.session.commit()
        return product

    def update(self, user_id: int, product_id: int, product_schema: ProductRequest) -> Product:
        product = self.get(product_id)
        for field, value in product_schema:
            setattr(product, field, value)
        setattr(product, 'modified_by', user_id)
        self.session.commit()
        return product

    def delete(self, product_id: int):
        product = self.get(product_id)
        self.session.delete(product)
        self.session.commit()
