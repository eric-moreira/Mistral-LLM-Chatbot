from datetime import datetime
from pymongo import MongoClient
import logging
import os

def get_mongo_uri():
    try:
        with open('/run/secrets/mongo_app_pass') as f:
            password = f.read().strip()
        return f"mongodb://chatbot_user:{password}@mongo:27017/chatbot_db"
    except Exception as e:
        logging.error(f"Failed to read MongoDB secret: {e}")
        return None

def save_message(speaker, message, session_id, chat_id, model="gpt-4o"):
    doc = {
        "session_id": session_id,
        "chat_id": chat_id,
        "timestamp": datetime.now(),
        "speaker": speaker,
        "message": message,
        "metadata": {
            "model": model,
            "source": "smol.py"
        }
    }
    collection.insert_one(doc)


def setup_mongo():
    global collection
    mongo_uri = get_mongo_uri()
    client = MongoClient(mongo_uri)
    db = client["chatbot_db"]
    collection = db["conversations"]
    return collection