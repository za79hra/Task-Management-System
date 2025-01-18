import jwt
import datetime
from app.config import Settings
from fastapi import HTTPException, status

import logging

USER_ROLE = ['admin', 'user']
ADMIN_ROLE = ['admin']
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def role_required(token: str, required_roles: list):
    try:
        logger.info(f"Verifying token: {token}")
        payload = verify_token(token, "access")
        if payload["role"] not in required_roles:
            logger.warning(f"Access forbidden for role: {payload['role']}")
            raise HTTPException(status_code=403, detail="Access forbidden")
        logger.info(f"Access granted for user with role: {payload['role']}")
        return payload  # Return the payload if the role is valid
    except Exception as e:
        logger.error(f"Error verifying token: {str(e)}")
        raise HTTPException(status_code=401, detail="Your access is not correct")


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
