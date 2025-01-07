from datetime import datetime

from app.config import Settings
from app.database.mongodb.task_dao import insert_task_query, get_user_for_assigned_task_query, \
    update_task_for_new_assigned_query, \
    get_user_for_task_id_query, delete_task_query


class TaskService:
    def __init__(self):

        self.number_allowed_tasks = Settings.NUM_ALLOWED_TASK

    async def create_new_task(self, task_data: dict):
        insert_time = datetime.now()
        task_data['insert_time'] = insert_time
        assigned_user_id = task_data['assigned_user_id']

        success_get, result_get = await get_user_for_assigned_task_query(assigned_user_id)
        if success_get:
            if len(result_get) >= self.number_allowed_tasks:
                return {"error": f"Maximum task limit reached ({self.number_allowed_tasks} tasks)", "status_code": 400}
            # print(self.number_allowed_tasks)
            success_insert, result_insert = await insert_task_query(task_data)
            if success_insert:
                return result_insert
            return {"message": "An unexpected error has occurred.", 'status_code': 417}
        success_insert_new, result_insert_new = await insert_task_query(task_data)
        if success_insert_new:
            return {"message": "the new task is successfully this is your first task", 'status_code': 200}
        return {"message": "An unexpected error has occurred.", 'status_code': 417}

    @staticmethod
    async def update_assigned_task(task_data):
        task_id = task_data['task_id']
        success_get, result_get = await get_user_for_task_id_query(task_id)
        if success_get:
            task_data['update_time'] = datetime.now()
            success_update, result_update = await update_task_for_new_assigned_query(task_id, task_data)
            return result_update
        return result_get

    @staticmethod
    async def get_one_assigned_task(task_id):
        success_get, result_get = await get_user_for_task_id_query(task_id)
        if success_get:
            return {f"data for task {task_id} is ": result_get, 'status_code': 200}
        return result_get

    @staticmethod
    async def delete_special_task(task_id):
        success_get, result_get = await get_user_for_task_id_query(task_id)
        if success_get:
            success = await delete_task_query(task_id)
            if success:
                return {"message": "The delete was successful", 'status_code': 200}
            return {"error": "An unexpected error has occurred", "status_code": 417}
        return result_get
