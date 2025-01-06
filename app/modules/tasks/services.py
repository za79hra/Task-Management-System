from datetime import datetime

from app.database.mongodb.task_dao import insert_task, get_user_for_assigned_task, update_task_for_new_assigned


async def create_new_task(task_data: dict):
    insert_time = datetime.now()
    task_data['insert_time'] = insert_time
    assigned_user_id = task_data['assigned_user_id']

    success_get, result_get = await get_user_for_assigned_task(assigned_user_id)
    if success_get:
        if len(result_get) >= 5:
            return {"error": "Maximum task limit reached (5 tasks)", "status_code": 400}

        success_insert, result_insert = await insert_task(task_data)
        if success_insert:
            return result_insert
        return {"message": "An unexpected error has occurred.", 'status_code': 417}


async def update_assigned_task(task_data):
    user_id = task_data['task_id']
    success_get, result_get = await get_user_for_assigned_task(user_id)
    if success_get:
        task_data['update_time'] = datetime.now()
        success_update, result_update = await update_task_for_new_assigned(user_id, task_data)
        return result_update
    return result_get
