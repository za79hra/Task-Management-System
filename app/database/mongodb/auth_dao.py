from app.database.mongodb.base_mongo import MongoConnection
from pymongo import errors
from bson import ObjectId
from datetime import datetime
from pymongo import ASCENDING


def create_ttl_index():
    with MongoConnection() as mongo:
        mongo.otp.create_index(
            [("created_at", ASCENDING)],
            expireAfterSeconds=120
        )


async def get_by_user_name(user_name: str):
    try:
        with MongoConnection() as mongo:
            user_data = mongo.users.find_one({"username": user_name})
            if user_data:
                return True, user_data

            return False, {'error': "not exist", 'status_code': 404}
    except errors:
        return False, {"error": "An error occurred on the server", "status_code": 500}
    except Exception:
        return False, {"error": "An unexpected error has occurred", "status_code": 417}


async def update_data_by_phone(data):
    try:
        _id = data['_id']

        data.pop('_id', None)

        with MongoConnection() as mongo:
            mongo.users.update_one(
                {"_id": ObjectId(_id)},
                {"$set": data},
                upsert=True
            )
        return True, {"message": "The operation was successful", 'status_code': 200}

    except errors:
        return False, {"error": "An error occurred on the server", "status_code": 500}
    except Exception:
        return False, {"error": "An unexpected error has occurred", "status_code": 417}


async def get_phone_number_query(data):
    try:
        with MongoConnection() as mongo:
            data = mongo.otp.find({"phone": data})
            list_data = list(data)
        if list_data:
            return True, list_data
        return False, {'error': "not exist", 'status_code': 404}
    except errors:
        return False, {"error": "An error occurred on the server", "status_code": 500}
    except Exception:
        return False, {"error": "An unexpected error has occurred", "status_code": 417}


async def update_data_(phone, otp):
    try:
        current_time = datetime.utcnow()
        with MongoConnection() as mongo:
            mongo.otp.update_one(
                {"phone": phone},
                {"$set": {
                    "phone": phone,
                    "otp": otp,
                    "is_verified": False,
                    "created_at": current_time
                }},
                upsert=True
            )
        return True, {"message": "The operation was successful", 'status_code': 200}
    except errors:
        return False, {"error": "An error occurred on the server", "status_code": 500}
    except Exception:
        return False, {"error": "An unexpected error has occurred", "status_code": 417}
