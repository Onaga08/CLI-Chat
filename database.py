# database.py
import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_DETAILS = os.getenv("MONGO_URI")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.chat_db
messages_collection = database.get_collection("messages")
