# app/schemas/order.py
from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal
from datetime import datetime

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = 1
    price_at_time: Decimal

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    order_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    total_amount: Decimal
    status: str = "pending"
    shipping_address: Optional[str] = None
    tracking_number: Optional[str] = None
    estimated_delivery_date: Optional[datetime] = None

class OrderCreate(OrderBase):
    user_id: int
    items: List[OrderItemCreate]

class Order(OrderBase):
    id: int
    user_id: int
    items: List[OrderItem] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True