import jwt
from datetime import datetime, timedelta
from app.config import settings

# def create_jwt_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
#     """
#     تولید توکن JWT
#     """
#     to_encode = data.copy()
#     expire = datetime.utcnow() + expires_delta
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm="HS256")
#     return encoded_jwt

# auth/auth_header.py

from fastapi import Depends, HTTPException
from typing import List, Tuple
from .auth_service import get_current_user  # فرض می‌شود این تابع اطلاعات کاربر را از توکن استخراج می‌کند


# class AuthHeader:
#     def __init__(self, role_names: List[str] = None, active: bool = True):
#         self.role_names = role_names
#         self.active = active
#
#     async def auth(self, current_user: dict = Depends(get_current_user)) -> Tuple[dict, dict]:
#         """
#         بررسی توکن و نقش کاربر برای دسترسی به بخش‌های مختلف
#         """
#         if not current_user:
#             raise HTTPException(status_code=401, detail="کاربر وارد نشده است")
#
#         # بررسی وضعیت فعال بودن حساب کاربری
#         if not self.active or not current_user.get("is_active"):
#             raise HTTPException(status_code=403, detail="حساب کاربری غیرفعال است")
#
#         # بررسی نقش‌های مجاز
#         if self.role_names and current_user.get("role") not in self.role_names:
#             raise HTTPException(status_code=403, detail="دسترسی غیرمجاز")
#
#         return current_user, {"access_token": "some_access_token", "refresh_token": "some_refresh_token"}
