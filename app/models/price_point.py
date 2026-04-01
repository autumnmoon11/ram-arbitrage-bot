# app/models/price_point.py
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional

class PricePoint(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    retailer: str
    product_name: str
    model_number: str = Field(index=True)
    price: float
    in_stock: bool
    url: str
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )