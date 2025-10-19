# فقط برای تست هش کردن — در محیط تولید استفاده نشه
from app.core.security import get_password_hash, verify_password

if __name__ == "__main__":
    password = "123456"
    hashed = get_password_hash(password)
    print("Hashed password:", hashed)
    print("Verify:", verify_password(password, hashed))  # باید True باشه