import os
import time
import requests

DATA_DIR = "data/"
PROCESSED_DIR = "data/processed/" 

if not os.path.exists(PROCESSED_DIR):
    os.makedirs(PROCESSED_DIR)

def monitor_and_trigger():
    print("🛰️ PulseWatchdog Active. Monitoring data/ folder...")
    while True:
        files = [f for f in os.listdir(DATA_DIR) if f.endswith(".pdf")]
        for file in files:
            print(f"🕵️ PulseArchitect: New document detected: {file}")
            
            requests.post("http://127.0.0.1:8000/chat", json={"message": f"New document added: {file}"})
            
            os.rename(os.path.join(DATA_DIR, file), os.path.join(PROCESSED_DIR, file))
            print(f"✅ {file} analyzed and moved to 'processed/' folder.")
            
        time.sleep(10) 

if __name__ == "__main__":
    monitor_and_trigger()