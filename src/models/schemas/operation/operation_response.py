from typing import Optional, List

from pydantic import BaseModel
from datetime import datetime
from src.models.schemas.tank.tank_response import TankResponse
from src.models.schemas.product.product_response import ProductResponse


class OperationResponse(BaseModel):
    id: int
    mass: float
    date_start: datetime
    date_end: datetime
    tank_id: int
    product_id: int
    created_at: datetime
    created_by: int
    modified_at: datetime
    modified_by: int

    class Config:
        orm_mode = True