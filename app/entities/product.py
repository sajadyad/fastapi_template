# app/models/product.py
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Numeric(precision=10, scale=2), nullable=False)
    file_type = Column(String, nullable=False)  # e.g., "dataset", "book"
    format = Column(String)
    writer = Column(String)
    release_date = Column(DateTime)
    status = Column(String, default="active")  # active, draft, deleted
    download_count = Column(Integer, default=0)
    rating_average = Column(Numeric(precision=3, scale=2), default=0.0)
    rating_count = Column(Integer, default=0)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False) 
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # رابطه با کاربر (مالک)
    owner = relationship("User", back_populates="owned_products")
 