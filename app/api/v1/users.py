# app/api/v1/users.py
from fastapi import APIRouter, HTTPException
from app.models import User
from app.database import users_collection
from pydantic import BaseModel

router = APIRouter()

class UserIn(BaseModel):
    username: str
    email: str

@router.post("/register", response_model=User)
async def register_user(user: UserIn):
    # Check if a user with the same username or email exists
    existing = await users_collection.find_one({
        "$or": [{"username": user.username}, {"email": user.email}]
    })
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    user_dict = user.dict()
    result = await users_collection.insert_one(user_dict)
    created_user = await users_collection.find_one({"_id": result.inserted_id})
    # Convert ObjectId to string for the response
    created_user["_id"] = str(created_user["_id"])
    return created_user
