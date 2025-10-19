# app/schemas/user.py
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None

class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class User(UserInDBBase):
    roles: List[str] = []  # فقط عنوان نقش‌ها

    @classmethod
    def from_orm(cls, user_orm):
        roles = [role.title for role in user_orm.roles]
        return cls(
            id=user_orm.id,
            username=user_orm.username,
            email=user_orm.email,
            first_name=user_orm.first_name,
            last_name=user_orm.last_name,
            phone=user_orm.phone,
            is_active=user_orm.is_active,
            created_at=user_orm.created_at,
            updated_at=user_orm.updated_at,
            roles=roles
        )