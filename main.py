from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from typing import Dict
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")
connected_users: Dict[str, WebSocket] = {}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, nickname: str = Query(...), token: str = Query(...)):
    if token != ADMIN_TOKEN:
        await websocket.close(code=1008)
        return

    if nickname in connected_users:
        await websocket.close(code=4000)
        return

    await websocket.accept()
    connected_users[nickname] = websocket

    await broadcast_system(f"{nickname} joined the chat")
    await send_user_list()

    try:
        while True:
            data = await websocket.receive_json()
            msg_type = data.get("type")

            if msg_type == "send":
                to_user = data.get("to")
                message = data.get("message")
                if to_user in connected_users:
                    await connected_users[to_user].send_json({
                        "type": "message",
                        "from": nickname,
                        "message": message
                    })
                else:
                    await websocket.send_json({
                        "type": "error",
                        "message": f"User '{to_user}' is not online"
                    })

            elif msg_type == "get-users":
                await websocket.send_json({
                    "type": "users",
                    "users": list(connected_users.keys())
                })

            elif msg_type == "ping":
                await websocket.send_json({
                    "type": "pong",
                    "message": "alive"
                })

            elif msg_type == "global":
                message = data.get("message")
                await broadcast_global(nickname, message)

    except WebSocketDisconnect:
        connected_users.pop(nickname, None)
        await broadcast_system(f"{nickname} left the chat")
        await send_user_list()

async def broadcast_system(message: str):
    for ws in connected_users.values():
        await ws.send_json({
            "type": "system",
            "message": message
        })

async def broadcast_global(sender: str, message: str):
    for ws in connected_users.values():
        await ws.send_json({
            "type": "global",
            "from": sender,
            "message": message
        })

async def send_user_list():
    user_list = list(connected_users.keys())
    for ws in connected_users.values():
        await ws.send_json({
            "type": "users",
            "users": user_list
        })