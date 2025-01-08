from datetime import datetime
from app.config import Settings
from app.database.mongodb.task_dao import insert_task_query, get_user_for_assigned_task_query, \
    update_task_for_new_assigned_query, \
    get_user_for_task_id_query, delete_task_query


class TaskService:
    def __init__(self):
        self.number_allowed_tasks = Settings.NUM_ALLOWED_TASK

    async def create_new_task(self, task_data: dict):
        """Creates a new task for the assigned user if they haven't reached the max limit."""
        assigned_user_id = task_data['assigned_user_id']

        # Check if the user has exceeded the allowed number of tasks
        user_task_count = await self.get_user_task_count(assigned_user_id)
        if user_task_count >= self.number_allowed_tasks:
            return {"error": f"Maximum task limit reached ({self.number_allowed_tasks} tasks)", "status_code": 400}

        # Add insertion time
        task_data['insert_time'] = datetime.now()

        # Insert the task into the database
        success_insert, result_insert = await self.insert_task(task_data)
        if success_insert:
            return result_insert
        return {"message": "An unexpected error has occurred.", 'status_code': 417}

    async def get_user_task_count(self, user_id: str):
        """Returns the number of tasks assigned to a user."""
        success_get, result_get = await get_user_for_assigned_task_query(user_id)
        if success_get:
            return len(result_get)
        return 0

    async def insert_task(self, task_data: dict):
        """Inserts a new task into the database."""
        success_insert, result_insert = await insert_task_query(task_data)
        if success_insert:
            return success_insert, result_insert
        return False, None

    async def update_assigned_task(self, task_data):
        """Updates the details of an assigned task."""
        task_id = task_data['task_id']
        success_get, result_get = await self.get_task_by_id(task_id)
        if success_get:
            task_data['update_time'] = datetime.now()
            success_update, result_update = await update_task_for_new_assigned_query(task_id, task_data)
            return result_update
        return result_get

    async def get_task_by_id(self, task_id: str):
        """Retrieves task data by task ID."""
        success_get, result_get = await get_user_for_task_id_query(task_id)
        return success_get, result_get

    async def get_one_assigned_task(self, task_id):
        """Gets the data for a specific task."""
        success_get, result_get = await self.get_task_by_id(task_id)
        if success_get:
            return {f"data for task {task_id} is ": result_get, 'status_code': 200}
        return result_get

    async def delete_special_task(self, task_id):
        """Deletes a specific task if it exists."""
        success_get, result_get = await self.get_task_by_id(task_id)
        if success_get:
            success = await delete_task_query(task_id)
            if success:
                return {"message": "The delete was successful", 'status_code': 200}
            return {"error": "An unexpected error has occurred", "status_code": 417}
        return result_get
