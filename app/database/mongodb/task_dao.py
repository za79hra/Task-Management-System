from app.database.mongodb.base_mongo import MongoConnection
from pymongo import errors
from bson import ObjectId


async def insert_task(task_data: dict):
    try:
        with MongoConnection() as mongo:
            mongo.users.insert_one(task_data)
        return True, {"message": "The operation was successful", 'status_code': 200}
    except errors:
        return False, {"error": "An error occurred on the server", "status_code": 500}
    except Exception:
        return False, {"error": "An unexpected error has occurred", "status_code": 417}


async def get_user_for_task_id(task_id: str):
    # try:
    with MongoConnection() as mongo:
        data = mongo.users.find_one({"_id": ObjectId(task_id)})
    if data:
        data['_id'] = str(data['_id'])
        return True, data
    return False, {'error': "not exist", 'status_code': 404}


# except errors:
#     return False, {"error": "An error occurred on the server", "status_code": 500}
# except Exception:
#     return False, {"error": "An unexpected error has occurred", "status_code": 417}

async def get_user_for_assigned_task(assigned_user_id: str):
    with MongoConnection() as mongo:
        data = list(mongo.users.find({"assigned_user_id": assigned_user_id}))
    if data:
        print(data)
        return True, data
    return False, {'error': "not exist", 'status_code': 404}


async def update_task_for_new_assigned(task_id, task_data):
    try:
        with MongoConnection() as mongo:
            result = mongo.users.update_one({'_id': ObjectId(task_id)}, {'$set': task_data})
            if result.modified_count > 0:
                return True, {"message": "The update was successful", 'status_code': 200}
            return False, {"message": "No document matched the query", 'status_code': 404}
    except errors:
        return False, {"error": "An error occurred on the server", "status_code": 500}
    except Exception:
        return False, {"error": "An unexpected error has occurred", "status_code": 417}
