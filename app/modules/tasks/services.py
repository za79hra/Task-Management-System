from datetime import datetime
from app.config import Settings
from app.database.mongodb.task_dao import insert_task_query, get_user_for_assigned_task_query, \
    update_task_for_new_assigned_query, \
    get_user_for_task_id_query, delete_task_query
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TaskService:
    def __init__(self):
        self.number_allowed_tasks = Settings.NUM_ALLOWED_TASK

    async def create_new_task(self, task_data: dict):
        """Creates a new task for the assigned user if they haven't reached the max limit."""
        assigned_user_id = task_data['assigned_user_id']
        logger.info(f"Attempting to create task for user {assigned_user_id}")

        # Check if the user has exceeded the allowed number of tasks
        user_task_count = await self.get_user_task_count(assigned_user_id)
        if user_task_count >= self.number_allowed_tasks:
            logger.warning(f"User {assigned_user_id} has exceeded the max task limit")
            return {"error": f"Maximum task limit reached ({self.number_allowed_tasks} tasks)", "status_code": 400}

        # Add insertion time
        task_data['insert_time'] = datetime.now()
        logger.info(f"Inserting task for user {assigned_user_id} at {task_data['insert_time']}")

        # Insert the task into the database
        success_insert, result_insert = await self.insert_task(task_data)
        if success_insert:
            logger.info(f"Task created successfully for user {assigned_user_id}")
            return result_insert
        logger.error(f"Failed to create task for user {assigned_user_id}")
        return {"message": "An unexpected error has occurred.", 'status_code': 417}

    async def get_user_task_count(self, user_id: str):
        """Returns the number of tasks assigned to a user."""
        success_get, result_get = await get_user_for_assigned_task_query(user_id)
        if success_get:
            logger.info(f"Found {len(result_get)} tasks for user {user_id}")
            return len(result_get)
        logger.warning(f"No tasks found for user {user_id}")
        return 0

    async def insert_task(self, task_data: dict):
        """Inserts a new task into the database."""
        try:
            logger.info(f"Inserting task: {task_data}")
            success_insert, result_insert = await insert_task_query(task_data)
            if success_insert:
                logger.info(f"Task inserted successfully: {task_data}")
                return success_insert, result_insert
            logger.error(f"Failed to insert task: {task_data}")
            return False, None
        except Exception as e:
            logger.exception(f"Error inserting task: {e}")
            return False, None

    async def update_assigned_task(self, task_data):
        """Updates the details of an assigned task."""
        task_id = task_data['task_id']
        logger.info(f"Attempting to update task with ID: {task_id}")

        success_get, result_get = await self.get_task_by_id(task_id)
        if success_get:
            task_data['update_time'] = datetime.now()
            logger.info(f"Updating task with ID: {task_id} at {task_data['update_time']}")
            success_update, result_update = await update_task_for_new_assigned_query(task_id, task_data)
            if success_update:
                logger.info(f"Task updated successfully with ID: {task_id}")
                return result_update
            logger.error(f"Failed to update task with ID: {task_id}")
            return {"message": "An unexpected error has occurred", 'status_code': 417}
        logger.warning(f"Task with ID: {task_id} not found")
        return result_get

    async def get_task_by_id(self, task_id: str):
        """Retrieves task data by task ID."""
        logger.info(f"Retrieving task with ID: {task_id}")
        success_get, result_get = await get_user_for_task_id_query(task_id)
        if success_get:
            logger.info(f"Task found with ID: {task_id}")
        else:
            logger.warning(f"Task with ID: {task_id} not found")
        return success_get, result_get

    async def get_one_assigned_task(self, task_id):
        """Gets the data for a specific task."""
        logger.info(f"Fetching details for task {task_id}")
        success_get, result_get = await self.get_task_by_id(task_id)
        if success_get:
            logger.info(f"Task data retrieved successfully for task {task_id}")
            return {f"data for task {task_id} is ": result_get, 'status_code': 200}
        logger.error(f"Failed to retrieve task {task_id}")
        return result_get

    async def delete_special_task(self, task_id):
        """Deletes a specific task if it exists."""
        logger.info(f"Attempting to delete task with ID: {task_id}")
        success_get, result_get = await self.get_task_by_id(task_id)
        if success_get:
            success = await delete_task_query(task_id)
            if success:
                logger.info(f"Task with ID {task_id} deleted successfully")
                return {"message": "The delete was successful", 'status_code': 200}
            logger.error(f"Failed to delete task with ID: {task_id}")
            return {"error": "An unexpected error has occurred", "status_code": 417}
        logger.warning(f"Task with ID: {task_id} not found for deletion")
        return result_get
