import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from astrapy import DataAPIClient
from app.services.agent import run_pulse_agent

app = FastAPI(title="PulseArchitect API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    return await run_pulse_agent(request.message)

@app.get("/tickets")
async def get_tickets():
    client = DataAPIClient()
    db = client.get_database(os.getenv("ASTRA_DB_API_ENDPOINT"), token=os.getenv("ASTRA_DB_APPLICATION_TOKEN"))
    tickets = list(db.get_collection("pulse_tickets").find({}))
    
    def safe_ts(x):
        try: return float(x.get('timestamp', 0))
        except: return 0
        
    tickets.sort(key=safe_ts, reverse=True)
    return tickets[:7]

@app.get("/activities")
async def get_activities():
    client = DataAPIClient()
    db = client.get_database(os.getenv("ASTRA_DB_API_ENDPOINT"), token=os.getenv("ASTRA_DB_APPLICATION_TOKEN"))
    activities = list(db.get_collection("ai_metrics").find({}))
    
    def safe_ts(x):
        try: return float(x.get('timestamp', 0))
        except: return 0
        
    activities.sort(key=safe_ts, reverse=True)
    return activities[:7]

@app.post("/reset")
async def reset_system():
    client = DataAPIClient()
    db = client.get_database(os.getenv("ASTRA_DB_API_ENDPOINT"), token=os.getenv("ASTRA_DB_APPLICATION_TOKEN"))
    db.get_collection("pulse_tickets").delete_many({})
    db.get_collection("ai_metrics").delete_many({})
    return {"status": "success"}