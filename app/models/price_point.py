# app/models/price_point.py
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class PricePoint(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    retailer: str
    product_name: str
    price: float
    in_stock: bool
    url: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)