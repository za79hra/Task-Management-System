import random
from fastapi import HTTPException
from fastapi import status
from app.database.mongodb.auth_dao import update_data_, get_phone_number_query, update_data_by_phone, get_by_user_name
from app.modules.auth.utils import create_tokens


async def create_random_otp():
    otp = str(random.randint(100000, 999999))
    return otp


async def set_otp_for_new_user(phone_number: str):
    success_check, result_check = await check_phone_for_existing_user(phone_number)
    if not success_check:
        otp = await create_random_otp()
        success, result = await update_data_(phone_number, otp)
        if success:
            return {"message": "OTP sent successfully", "otp": otp, 'status_code': 200}
        return result
    return {"message": "your phone is already exist", 'status_code': 401}


async def check_phone_for_existing_user(phone_number):
    success, result = await get_phone_number_query(phone_number)
    if success:
        return True, result
    return False, {"message": "this is first login", 'status_code': 200}


async def set_user_and_register(data):
    success, result = await check_phone_for_existing_user(data['phone'])
    if success:
        user_data = result[0]
        if user_data["is_verified"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already registered")
        if data['otp'] != user_data['otp']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP")

        new_data = {
            "_id": user_data['_id'],
            "phone": user_data['phone'],
            "username": data['username'],
            "password": data['password'],
            "is_verified": True,
            "role": data['role']
        }
        success, result = await update_data_by_phone(new_data)
        if success:
            return {"message": "User registered successfully", 'status_code': 200}
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to register user")


async def set_token_and_register(register_data):
    success, result = await get_by_user_name(register_data['username'])
    if success:
        if register_data['username'] != result['username'] or register_data['password'] != result['password']:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
        token = await set_token(result)
        return token


async def set_token(user):
    access_token, refresh_token = create_tokens(str(user["_id"]), user["role"])
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
