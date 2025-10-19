# app/auth/dependencies.py
from fastapi import Depends, HTTPException, status, Path
from datetime import datetime

from app.auth.engine import ABACEngine
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.user import User
from app.entities.product import Product
from app.core.auth import (
    get_current_user,
    get_current_product,
    get_purchased_product_ids,
)


engine = ABACEngine()

"""
# -------------------- FAKE USER & PRODUCT (موقت) --------------------
def get_current_user2():
    # بعداً این از توکن و دیتابیس میاد
    return {
        "id": 20,
        "username": "seller_user",
        "roles": ["seller"],
        "purchased_product_ids": [101, 102],
    }

def get_product(product_id: int = Path(...)):
    # بعداً این از دیتابیس میاد
    # فرض: محصول با id=100 متعلق به کاربر 20 هست
    return {
        "id": product_id,
        "owner_id": 20,
        "is_public": False,
        "type": "product",  # مهم برای ساخت policy_name
    }

# -------------------- AUTHORIZATION DEPENDENCY --------------------

"""


def authorize(action: str, resource_type: str):
    async def dependency(
        current_product: Product = Depends(get_current_product),
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ):
        purchased_ids = await get_purchased_product_ids(db, current_user.id)

        context = {
            "user": current_user,
            "resource": {
                "id": current_product.id,
                "owner_id": current_product.owner_id,
                "is_public": current_product.is_public,
                "type": "product",
            },
            "action": action,
            "env": {"hour": datetime.utcnow().hour, "purchased_ids": purchased_ids},
        }

        print("🟢 DEBUG: current_user.id:", current_user.id)
        print("🟢 DEBUG: current_product.owner_id:", current_product.owner_id)
        print("🟢 DEBUG: hour:", context["env"]["hour"])

        allowed = engine.check_access(context)
        if not allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied for '{action}' on '{resource_type}'",
            )
        return True

    return dependency
