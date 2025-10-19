# entities
from app.db.base import Base
from .item import Item
from .user import User
from .role import Role
from .audit import AuditLog
from .product import Product
from .order import Order,  OrderItem
from .associations import user_role
# این کار باعث می‌شود هنگام ایمپورت Base، مدل‌ها ثبت شوند
# app/models/__init__.py



