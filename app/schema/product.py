# app/schemas/product.py
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal
    file_type: str
    format: Optional[str] = None
    writer: Optional[str] = None
    release_date: Optional[datetime] = None
    status: str = "active"
    is_public: bool = False

class ProductCreate(ProductBase):
    owner_id: int

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    is_public: Optional[bool] = None
    status: Optional[str] = None

class ProductInDBBase(ProductBase):
    id: int
    owner_id: int
    download_count: int = 0
    rating_average: Decimal = Decimal("0.00")
    rating_count: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Product(ProductInDBBase):
    pass