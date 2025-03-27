# app/api/v1/websocket.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict
from app.models import Message
from app.database import messages_collection
from datetime import datetime

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        # mappping of user_id to WebSocket connection
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    async def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def broadcast_users(self):
        user_list = list(self.active_connections.keys())
        data = {"type": "user_list", "users": user_list}
        for ws in self.active_connections.values():
            await ws.send_json(data)

    async def broadcast_message(self, data: dict):
        # Broadcast a chat message to all connected clients
        for ws in self.active_connections.values():
            await ws.send_json(data)

manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    # need certificate details for extracting user_id
    user_id = websocket.headers.get("x-ssl-subject")
    if not user_id:
        # fallback
        await websocket.close(code=1008)
        return

    await manager.connect(user_id, websocket)
    await manager.broadcast_users()

    try:
        while True:
            data = await websocket.receive_json()
            message = Message(**data)
            await messages_collection.insert_one(message.dict())
            await manager.broadcast_message({
                "sender": message.sender,
                "message": message.message,
                "timestamp": message.timestamp.isoformat()
            })
    except WebSocketDisconnect:
        await manager.disconnect(user_id)
        # Broadcast updated user list upon disconnection
        await manager.broadcast_users()
