import os
from astrapy import DataAPIClient
from datetime import datetime

def log_metrics(token_count, energy, water):
    try:
        client = DataAPIClient()
        db = client.get_database(os.getenv("ASTRA_DB_API_ENDPOINT"), token=os.getenv("ASTRA_DB_APPLICATION_TOKEN"))
        
        collection = db.get_collection("ai_metrics")
        
        collection.insert_one({
            "timestamp": datetime.now().isoformat(),
            "tokens": token_count,
            "energy_kwh": energy,
            "water_liters": water,
            "date": datetime.now().strftime("%Y-%m-%d")
        })
        return True
    except Exception as e:
        print(f"Metrics DB Error: {e}")
        return False