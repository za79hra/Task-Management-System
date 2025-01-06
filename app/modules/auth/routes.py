# from fastapi import APIRouter, HTTPException, Depends
# from app.modules.auth.schemas import UserCreate, UserLogin
# from app.modules.auth.services import create_user, login_user
#
# auth_router = APIRouter()
#
# @auth_router.post("/register")
# def register(user: UserCreate):
#     return create_user(user)
#
# @auth_router.post("/login")
# def login(user: UserLogin):
#     return login_user(user)
