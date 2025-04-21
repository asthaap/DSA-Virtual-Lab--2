from pymongo import MongoClient
import os

def get_db():
    client = MongoClient(os.getenv("MONGODB_URI"))
    return client.get_database()

db = get_db()
submissions_collection = db["submissions"]
problems_collection = db["problems"]