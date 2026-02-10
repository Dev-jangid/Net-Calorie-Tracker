"""
MongoDB Connection Module
STEP 0: Empty skeleton - just the connection file structure
"""

from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# MongoDB connection placeholder
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "calorie_tracker")

# MongoDB connection client
_client = None

def get_client():
    """
    Get or create MongoDB client
    """
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI)
    return _client

def get_database():
    """
    Get MongoDB database instance
    """
    client = get_client()
    return client[DB_NAME]

def get_collection(collection_name):
    """
    Get a specific collection from the database
    """
    db = get_database()
    return db[collection_name]
