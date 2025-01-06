from fastapi import APIRouter, HTTPException, Depends, Response

# from app.modules.auth.utils import AuthHeader
from app.modules.tasks.models import TaskBase
from app.database.mongodb.task_dao import insert_task
from app.modules.tasks.services import create_new_task, update_assigned_task

app = APIRouter()


@app.post("/createtask")
async def create_task(
        response: Response,
        task: TaskBase,
        # auth_data=Depends(AuthHeader(role_names=['admin'], active=True).auth)
):
    # try:
    # customer_data, token = auth_data
    # response.headers["accessToken"] = token.get("access_token")
    # response.headers["refreshToken"] = token.get("refresh_token")
    # user_id = customer_data.get('user_id')
    # role = customer_data.get('role')
    task_data = task.dict()
    result = await create_new_task(task_data)
    response.status_code = result.get("status_code")
    return result


# except Exception:
#     raise HTTPException(status_code=500)
@app.put("/updatetask")
async def update_task(
        response: Response,
        task_id,
        task: TaskBase

):

    task_data = task.dict()
    task_data["task_id"] = task_id
    result = await update_assigned_task(task_data)
    response.status_code = result.get("status_code")
    return result
