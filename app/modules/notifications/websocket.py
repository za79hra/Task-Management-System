from fastapi import APIRouter, WebSocket, WebSocketDisconnect

websocket_router = APIRouter()
connections = []

@websocket_router.websocket("/notify")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            for connection in connections:
                await connection.send_text(data)
    except WebSocketDisconnect:
        connections.remove(websocket)
