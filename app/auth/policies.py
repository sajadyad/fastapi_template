# app/auth/policies.py
from typing import Any, Dict, Tuple
from .utils import is_admin, get_attr


def can_delete_product(user: Any, resource: Any, env: Dict[str, Any]) -> Tuple[bool, str]:
    """
    قوانین حذف محصول:
    - admin همیشه مجاز است.
    - مالک محصول (owner_id == user.id) در ساعات کاری (8 تا 23) مجاز است.
    """
    if is_admin(user):
        return True, "user_is_admin"

    user_id = get_attr(user, "id")
    owner_id = get_attr(resource, "owner_id")
    hour = env.get("hour", 0)

    if user_id == owner_id:
        if 8 <= hour < 23:
            return True, "owner_and_time_ok"
        else:
            return False, "owner_but_out_of_allowed_hours"

    return False, "not_owner_or_admin"


def can_download_product(user: Any, resource: Any, env: Dict[str, Any]) -> Tuple[bool, str]:
    """
    قوانین دانلود:
    - admin همیشه مجاز است.
    - اگر محصول عمومی باشد (is_public=True).
    - اگر کاربر مالک محصول باشد
    - اگر کاربر آن را خریده باشد (product.id در purchased_product_ids باشد).
    """
    if is_admin(user):
        return True, "user_is_admin"

    if get_attr(resource, "is_public", False):
        return True, "resource_is_public"
    
    if get_attr(user, "id") == get_attr(resource, "owner_id"):
        return True, "user_is_owner"

    product_id = get_attr(resource, "id")
    purchased_ids = env.get("purchased_ids", set())

    if product_id in purchased_ids:
        return True, "user_purchased"

    return False, "not_purchased_or_public"