from fastapi import status
import jwt
import datetime
from fastapi import HTTPException
from app.config import Settings


def create_tokens(user_id: str, role: str):
    current_time = datetime.datetime.utcnow()

    access_token_payload = {
        "user_id": user_id,
        "role": role,
        "exp": current_time + datetime.timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        "type": "access"
    }
    access_token = jwt.encode(access_token_payload, Settings.SECRET_KEY, algorithm="HS256")

    refresh_token_payload = {
        "user_id": user_id,
        "exp": current_time + datetime.timedelta(days=Settings.REFRESH_TOKEN_EXPIRE_DAYS),
        "type": "refresh"
    }
    refresh_token = jwt.encode(refresh_token_payload, Settings.SECRET_KEY, algorithm="HS256")

    return access_token, refresh_token


def verify_token(token: str, token_type: str):
    try:
        payload = jwt.decode(token, Settings.SECRET_KEY, algorithms=["HS256"])
        if payload.get("type") != token_type:
            raise jwt.InvalidTokenError("Invalid token type")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
