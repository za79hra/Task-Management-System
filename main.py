from fastapi import FastAPI
from app.modules.tasks.routes import app as api_router

app = FastAPI(title="Task Manager")

app.include_router(api_router, prefix="/task", tags=["Task"])


@app.get("/")
def root():
    return {"message": "Welcome to the Task Manager API "}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
