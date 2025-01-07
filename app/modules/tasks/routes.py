from fastapi import APIRouter, HTTPException, Depends, Response
from app.modules.tasks.models import TaskBase
from app.modules.tasks.services import TaskService

app = APIRouter()
service = TaskService()


@app.post("/createtask")
async def create_task(
        response: Response,
        task: TaskBase,

):
    try:
        task_data = task.dict()
        result = await service.create_new_task(task_data)
        response.status_code = result.get("status_code")
        return result
    except Exception:
        raise HTTPException(status_code=500)


@app.put("/updatetask")
async def update_task(
        response: Response,
        task_id,
        task: TaskBase

):
    try:
        task_data = task.dict()
        task_data["task_id"] = task_id
        result = await service.update_assigned_task(task_data)
        response.status_code = result.get("status_code")
        return result
    except Exception:
        raise HTTPException(status_code=500)


@app.get("/gettask")
async def get_task(
        response: Response,
        task_id
):
    try:
        result = await service.get_one_assigned_task(task_id)
        response.status_code = result.get("status_code")
        return result
    except Exception:
        raise HTTPException(status_code=500)


@app.delete("/deletetask")
async def delete_task(
        response: Response,
        task_id,

):
    try:
        result = await service.delete_special_task(task_id)
        response.status_code = result.get("status_code")
        return result
    except Exception:
        raise HTTPException(status_code=500)
