from fastapi import APIRouter, Response
from fastapi import HTTPException
from app.database.mongodb.auth_dao import create_ttl_index
from app.modules.auth.models import LoginUser, PhoneNumber, RegisterUser
from app.modules.auth.services import set_otp_for_new_user, set_user_and_register, set_token_and_register

app = APIRouter()


@app.post("/send-otp")
async def send_otp(
        response: Response,
        phone_number: PhoneNumber
):
    try:
        create_ttl_index()
        result = await set_otp_for_new_user(phone_number.phone)
        response.status_code = result.get("status_code")
        return result
    except Exception:
        raise HTTPException(status_code=500)


@app.post("/register")
async def register_user(
        register_model: RegisterUser,
        response: Response,

):
    try:
        data = register_model.dict()
        result = await set_user_and_register(data)
        response.status_code = result.get("status_code")
        return result

    except Exception:
        raise HTTPException(status_code=500)


@app.post("/token")
async def login(
        data: LoginUser,
        response: Response,
):
    try:
        register_data = data.dict()
        result = await set_token_and_register(register_data)
        response.status_code = result.get("status_code")
        return result

    except Exception:
        raise HTTPException(status_code=500)
