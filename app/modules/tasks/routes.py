from fastapi import APIRouter, HTTPException, Response

import logging
from app.modules.auth.utils import role_required
from app.modules.tasks.models import TaskBase
from app.modules.tasks.services import TaskService

USER_ROLE = ['admin', 'user']
ADMIN_ROLE = ['admin']
app = APIRouter()
service = TaskService()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.post("/createtask")
async def create_task(
        response: Response,
        task: TaskBase,
        token: str,

):
    try:
        logger.info(f"Creating task for user with token: {token}")
        user_payload = await role_required(token, ADMIN_ROLE)
        logger.info(f"User payload: {user_payload}")
        # print(user_payload)
        task_data = task.dict()
        result = await service.create_new_task(task_data)
        response.status_code = result.get("status_code")
        logger.info(f"Try Task created  with result: {result}")
        return result
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        raise HTTPException(status_code=500)


@app.put("/updatetask")
async def update_task(
        response: Response,
        task_id,
        task: TaskBase,
        token: str,

):
    try:
        logger.info(f"Updating task for user with token: {token}")
        user_payload = await role_required(token, ADMIN_ROLE)
        logger.info(f"User payload: {user_payload}")
        logger.info(f"Updating task with ID: {task_id}")
        task_data = task.dict()
        task_data["task_id"] = task_id
        result = await service.update_assigned_task(task_data)
        response.status_code = result.get("status_code")
        logger.info(f"Task updated successfully with result: {result}")
        return result
    except Exception as e:
        logger.error(f"Error updating task: {str(e)}")
        raise HTTPException(status_code=500)


@app.get("/gettask")
async def get_task(
        response: Response,
        task_id,
        token: str,
):
    try:

        user_payload = await role_required(token, USER_ROLE)
        logger.info(f"User payload: {user_payload}")
        logger.info(f"Fetching task with ID: {task_id}")
        result = await service.get_one_assigned_task(task_id)
        response.status_code = result.get("status_code")
        logger.info(f"Task fetched successfully with result: {result}")
        return result
    except Exception as e:
        logger.error(f"Error fetching task: {str(e)}")
        raise HTTPException(status_code=500)


@app.delete("/deletetask")
async def delete_task(
        response: Response,
        task_id,
        token: str,

):
    try:
        user_payload = await role_required(token, ADMIN_ROLE)
        logger.info(f"User payload: {user_payload}")
        logger.info(f"Deleting task with ID: {task_id}")
        result = await service.delete_special_task(task_id)
        response.status_code = result.get("status_code")
        logger.info(f"Task deleted successfully with result: {result}")
        return result
    except Exception as e:
        logger.error(f"Error deleting task: {str(e)}")
        raise HTTPException(status_code=500)
