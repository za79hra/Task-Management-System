# from fastapi import FastAPI
# from app.modules.auth.routes import auth_router
# from app.modules.tasks.routes import task_router
# from app.modules.notifications.websocket import websocket_router
#
# app = FastAPI(title="Task Manager")
#
# # ثبت مسیرهای API
# app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
# app.include_router(task_router, prefix="/tasks", tags=["Tasks"])
# app.include_router(websocket_router, prefix="/ws", tags=["WebSocket"])
#
# @app.get("/")
# def root():
#     return {"message": "Welcome to the Task Manager API"}
