from db.mongo import get_collection
from models.user_model import User
from bson import ObjectId

COLLECTION_NAME = "users"

def create_user(user: User):
    """
    Insert a new user into the database.
    """
    collection = get_collection(COLLECTION_NAME)
    user_dict = user.to_dict()
    result = collection.insert_one(user_dict)
    return str(result.inserted_id)

def get_all_users():
    """
    Retrieve all users from the database.
    """
    collection = get_collection(COLLECTION_NAME)
    users_data = collection.find()
    return [User.from_dict(u) for u in users_data]

def get_user_by_id(user_id: str):
    """
    Retrieve a user by their ID.
    """
    collection = get_collection(COLLECTION_NAME)
    user_data = collection.find_one({"_id": ObjectId(user_id)})
    if user_data:
        return User.from_dict(user_data)
    return None

def delete_user(user_id: str):
    """
    Delete a user by their ID.
    """
    collection = get_collection(COLLECTION_NAME)
    result = collection.delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count > 0
