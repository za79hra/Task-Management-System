from pydantic import BaseModel, field_validator
import re


class UserLogin(BaseModel):
    username: str
    password: str


class PhoneNumber(BaseModel):
    phone: str

    @field_validator('phone')
    def validate_phone(cls, v):
        if not re.match(r"^(?:\+98|0)9\d{9}$", v):
            raise ValueError("Invalid phone number format. Use +989XXXXXXXXX or 09XXXXXXXXX.")
        return v


class RegisterUser(BaseModel):
    phone: str
    username: str
    password: str
    otp: str
    role: str


class LoginUser(BaseModel):
    username: str
    password: str
