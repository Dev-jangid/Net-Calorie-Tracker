import sys
import os
import pandas as pd

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.mongo import get_collection

COLLECTION_NAME = "foods"

def load_foods():
    file_path = "data-excels-for-db/food-calories.xlsx"
    print(f"Loading food data from {file_path}...")
    
    try:
        df = pd.read_excel(file_path)
        # Assuming columns: Food Name, Serving Size, Calories per Serving Size
        # Normalize column names to match model if necessary
        
        records = df.to_dict('records')
        
        collection = get_collection(COLLECTION_NAME)
        # Clear existing data
        collection.delete_many({})
        
        result = collection.insert_many(records)
        print(f"Successfully loaded {len(result.inserted_ids)} food items.")
        
    except Exception as e:
        print(f"Error loading food data: {e}")

if __name__ == "__main__":
    load_foods()
