from pydantic import BaseModel
from datetime import datetime

class ProductResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    created_by: str
    modified_at: datetime
    modified_by: str

    class Config:
        orm_mode = True
