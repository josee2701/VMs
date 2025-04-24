# utils/ws_broadcaster.py
from fastapi import WebSocket, WebSocketDisconnect

from .ws_manager import ConnectionManager

manager = ConnectionManager()

async def websocket_ws_endpoint(websocket: WebSocket):
    """
    Mismo código que tenías en main.py,
    pero ahora aquí y usando el manager de este módulo.
    """
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
