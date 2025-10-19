from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.exceptions import ValidationException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.entities.user import User
from app.entities.product import Product

from app.auth.dependencies import authorize
from app.auth.engine import ABACEngine
from app.core.config import settings
from app.schema.response import success , failure

from app.core.auth import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
    authenticate_user,
    get_current_product
)

router = APIRouter()



engine = ABACEngine()

# Mock user DB (replace with real DB in production)
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "hashed_password": get_password_hash("secret"),
    }
}




class LoginResponse(BaseModel):
    access_token: str
    token_type: str


@router.post("/login",)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), 
                                 db: AsyncSession = Depends(get_db)
                                 ):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        claims={"sub": form_data.username}, 
        expires_delta=access_token_expires)

    return success(
        {"access_token": access_token, "token_type": "bearer"},
        flat=True,  
        )

@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/get_product/{product_id}")
async def get_product(current_product: Product = Depends(get_current_product)):
    return current_product


@router.delete("/delete-product/{product_id}", dependencies=[Depends(authorize("delete", "product"))])
async def delete_product(product_id: int):
    return {"message": f"Product {product_id} deleted successfully"}


@router.get("/download-product/{product_id}", dependencies=[Depends(authorize("download", "product"))])
async def download_product(product_id: int):
    return {"message": "Download allowed"}







# app/controller/auth.py

from sqlalchemy import select
from app.entities.role import Role
from app.entities.order import Order, OrderItem



@router.post("/seed", tags=["debug"])
async def seed_test_data(db: AsyncSession = Depends(get_db)):
    """
    فقط برای محیط توسعه!
    این route داده‌های تست زیر را ایجاد می‌کند:
    - نقش‌ها: admin, seller, user
    - کاربران: admin_user, seller_ali, buyer_reza
    - محصولات: 
        - Private Dataset (مالک: seller_ali, is_public=False)
        - Public Book (مالک: seller_ali, is_public=True)
    - سفارش: buyer_reza محصول خصوصی را خریده است
    """

    # ---------- 1. ایجاد نقش‌ها ----------
    roles_to_create = ["admin", "seller", "user"]
    for role_title in roles_to_create:
        result = await db.execute(select(Role).where(Role.title == role_title))
        if not result.scalar_one_or_none():
            role = Role(title=role_title, description=f"{role_title} role")
            db.add(role)
    await db.commit()

    # ---------- 2. دریافت نقش‌ها به صورت object ----------
    result = await db.execute(select(Role))
    roles = {role.title: role for role in result.scalars().all()}

    # ---------- 3. ایجاد کاربران ----------
    users_data = [
        {
            "username": "admin_user",
            "email": "admin@example.com",
            "password": "123456",
            "roles": [roles["admin"]],
        },
        {
            "username": "seller_ali",
            "email": "ali@example.com",
            "password": "123456",
            "roles": [roles["seller"]],
        },
        {
            "username": "buyer_reza",
            "email": "reza@example.com",
            "password": "123456",
            "roles": [roles["user"]],
        },
    ]

    created_users = {}
    for ud in users_data:
        result = await db.execute(select(User).where(User.username == ud["username"]))
        user = result.scalar_one_or_none()
        if not user:
            user = User(
                username=ud["username"],
                email=ud["email"],
                password_hash=get_password_hash(ud["password"]),
                first_name=ud["username"].split("_")[1].title()
                if "_" in ud["username"]
                else ud["username"],
                is_active=True,
            )
            user.roles = ud["roles"]
            db.add(user)
            await db.flush()  # دریافت id قبل از commit
        created_users[ud["username"]] = user

    await db.commit()

    # ---------- 4. ایجاد محصولات ----------
    products_data = [
        {
            "name": "Private Dataset",
            "description": "A private dataset for buyers only",
            "price": 50.00,
            "file_type": "dataset",
            "owner_id": created_users["seller_ali"].id,
            "is_public": False,
        },
        {
            "name": "Public Book",
            "description": "A free public book for everyone",
            "price": 0.00,
            "file_type": "book",
            "owner_id": created_users["seller_ali"].id,
            "is_public": True,
        },
    ]

    for pd in products_data:
        result = await db.execute(select(Product).where(Product.name == pd["name"]))
        if not result.scalar_one_or_none():
            product = Product(**pd)
            db.add(product)

    await db.commit()

    # ---------- 5. ایجاد سفارش (برای تست purchased) ----------
    result = await db.execute(select(Product).where(Product.name == "Private Dataset"))
    private_product = result.scalar_one_or_none()

    if private_product and "buyer_reza" in created_users:
        existing_order = await db.execute(
            select(Order)
            .join(OrderItem)
            .where(Order.user_id == created_users["buyer_reza"].id)
            .where(OrderItem.product_id == private_product.id)
        )
        if not existing_order.scalar_one_or_none():
            order = Order(
                user_id=created_users["buyer_reza"].id,
                total_amount=private_product.price,
                status="paid",
            )
            db.add(order)
            await db.flush()

            order_item = OrderItem(
                order_id=order.id,
                product_id=private_product.id,
                quantity=1,
                price_at_time=private_product.price,
            )
            db.add(order_item)

    await db.commit()

    # ---------- 6. واکشی نهایی برای نمایش اطلاعات ----------
    result = await db.execute(select(Product))
    all_products = result.scalars().all()

    product_list = [
        {"id": p.id, "name": p.name, "is_public": p.is_public} for p in all_products
    ]

    return {
        "message": "✅ Test data seeded successfully!",
        "users": list(created_users.keys()),
        "products": product_list,
        "note": "Use /api/v1/auth/login to get tokens and test ABAC rules.",
    }
