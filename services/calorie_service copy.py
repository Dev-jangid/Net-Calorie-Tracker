# from db.mongo import get_collection
# from models.food_model import Food
# from models.activity_model import Activity
# from models.log_model import DailyLog
# from bson import ObjectId
# from typing import List, Optional

# FOOD_COLLECTION = "foods"
# LOG_COLLECTION = "daily_logs"
# ACTIVITY_COLLECTION = "activities"

# def get_all_foods() -> List[Food]:
#     """
#     Fetch all food items from the database.
#     """
#     collection = get_collection(FOOD_COLLECTION)
#     foods_data = collection.find()
#     return [Food.from_dict(f) for f in foods_data]

# def get_food_by_id(food_id: str) -> Optional[Food]:
#     """
#     Fetch a specific food by its ID.
#     """
#     collection = get_collection(FOOD_COLLECTION)
#     food_data = collection.find_one({"_id": ObjectId(food_id)})
#     if food_data:
#         return Food.from_dict(food_data)
#     return None

# def get_all_activities() -> List[Activity]:
#     """
#     Fetch all activity items from the database.
#     """
#     collection = get_collection(ACTIVITY_COLLECTION)
#     activities_data = collection.find()
#     return [Activity.from_dict(a) for a in activities_data]

# def get_activity_by_id(activity_id: str) -> Optional[Activity]:
#     """
#     Fetch a specific activity by its ID.
#     """
#     collection = get_collection(ACTIVITY_COLLECTION)
#     activity_data = collection.find_one({"_id": ObjectId(activity_id)})
#     if activity_data:
#         return Activity.from_dict(activity_data)
#     return None

# def save_daily_log(log: DailyLog):
#     """
#     Save or update a daily log in the database.
#     """
#     collection = get_collection(LOG_COLLECTION)
#     log_dict = log.to_dict()
    
#     # Check if a log already exists for this user and date
#     existing_log = collection.find_one({"user_id": log.user_id, "date": log.date})
    
#     if existing_log:
#         collection.update_one(
#             {"_id": existing_log["_id"]},
#             {"$set": log_dict}
#         )
#         return str(existing_log["_id"])
#     else:
#         result = collection.insert_one(log_dict)
#         return str(result.inserted_id)

# def get_daily_log(user_id: str, date_str: str) -> Optional[DailyLog]:
#     """
#     Retrieve a daily log for a specific user and date.
#     """
#     collection = get_collection(LOG_COLLECTION)
#     log_data = collection.find_one({"user_id": user_id, "date": date_str})
#     if log_data:
#         return DailyLog.from_dict(log_data)
#     return None

# def delete_daily_log(user_id: str, date_str: str) -> bool:
#     """
#     Delete a daily log for a specific user and date.
#     """
#     collection = get_collection(LOG_COLLECTION)
#     result = collection.delete_one({"user_id": user_id, "date": date_str})
#     return result.deleted_count > 0

# def delete_food_entry(log: DailyLog, index: int):
#     """
#     Remove a food entry by index and update the log.
#     """
#     if 0 <= index < len(log.foods):
#         removed_food = log.foods.pop(index)
#         # Recalculate net calories
#         total_in = sum(f.calories for f in log.foods)
#         total_out = sum(a.calories_burnt for a in log.activities)
#         log.net_calories = total_in - log.bmr_at_time - total_out
#         save_daily_log(log)
#         return True
#     return False

# def delete_activity_entry(log: DailyLog, index: int):
#     """
#     Remove an activity entry by index and update the log.
#     """
#     if 0 <= index < len(log.activities):
#         removed_act = log.activities.pop(index)
#         # Recalculate net calories
#         total_in = sum(f.calories for f in log.foods)
#         total_out = sum(a.calories_burnt for a in log.activities)
#         log.net_calories = total_in - log.bmr_at_time - total_out
#         save_daily_log(log)
#         return True
#     return False
