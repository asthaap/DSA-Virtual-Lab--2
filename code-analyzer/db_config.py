from pymongo import MongoClient
import os

def get_db():
    client = MongoClient(os.getenv("MONGODB_URI"))
    return client.get_database()

db = get_db()
problems_collection = db["problems"]
submissions_collection = db["submissions"]