from typing import Optional
from pydantic import BaseModel


class ProductRequest(BaseModel):
    name: str

