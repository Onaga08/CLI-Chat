# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import users, websocket

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers for our API endpoints
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(websocket.router, prefix="/api/v1", tags=["websocket"])

@app.get("/")
async def root():
    return {"message": "FastAPI Chat Server Running"}
