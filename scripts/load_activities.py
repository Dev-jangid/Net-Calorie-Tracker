import sys
import os
import pandas as pd

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.mongo import get_collection

COLLECTION_NAME = "activities"

def load_activities():
    file_path = "data-excels-for-db/MET-values.xlsx"
    print(f"Loading activity data from {file_path}...")
    
    try:
        df = pd.read_excel(file_path)
        # Assuming columns: Activity Name, Specific Motion, MET Value
        
        records = df.to_dict('records')
        
        collection = get_collection(COLLECTION_NAME)
        # Clear existing data
        collection.delete_many({})
        
        result = collection.insert_many(records)
        print(f"Successfully loaded {len(result.inserted_ids)} activities.")
        
    except Exception as e:
        print(f"Error loading activity data: {e}")

if __name__ == "__main__":
    load_activities()
