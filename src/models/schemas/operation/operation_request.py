from typing import Optional
from pydantic import BaseModel


class OperationRequest(BaseModel):
    mass: float
    date_start: str
    date_end: str
    tank_id: int
    product_id: int
