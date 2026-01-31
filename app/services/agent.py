import os
import json
import asyncio
import traceback
import re
import time
from dotenv import load_dotenv

from beeai_framework.backend import (
    ChatModelParameters, UserMessage, SystemMessage, ToolMessage, MessageToolResultContent
)
from beeai_framework.adapters.watsonx.backend.chat import WatsonxChatModel
from beeai_framework.tools.tool import tool
from astrapy import DataAPIClient 

from app.services.optimizer import AIResourceOptimizer
from app.services.notifier import PulseNotifier 

load_dotenv()
optimizer = AIResourceOptimizer()

async def prune_collection(collection_name, limit=7):
    try:
        client = DataAPIClient()
        db = client.get_database(os.getenv("ASTRA_DB_API_ENDPOINT"), token=os.getenv("ASTRA_DB_APPLICATION_TOKEN"))
        collection = db.get_collection(collection_name)
        docs = list(collection.find({}))
        
        def safe_sort(x):
            try: return float(x.get('timestamp', 0))
            except: return 0

        docs.sort(key=safe_sort, reverse=True)
        if len(docs) > limit:
            for doc in docs[limit:]:
                collection.delete_one({"_id": doc['_id']})
    except:
        pass

@tool
def search_docs(query: str):
    """Search corporate strategy documents for risk and budget data."""
    try:
        client = DataAPIClient()
        db = client.get_database(os.getenv("ASTRA_DB_API_ENDPOINT"), token=os.getenv("ASTRA_DB_APPLICATION_TOKEN"))
        collection = db.get_collection("pulse_docs")
        results = list(collection.find({}, limit=3))
        return "\n".join([r.get("text", "") for r in results])
    except:
        return "Memory access error."

async def execute_ticket_creation(title: str):
    try:
        client = DataAPIClient()
        db = client.get_database(os.getenv("ASTRA_DB_API_ENDPOINT"), token=os.getenv("ASTRA_DB_APPLICATION_TOKEN"))
        collection = db.get_collection("pulse_tickets")
        collection.insert_one({
            "title": title, 
            "status": "ACTIVE RISK", 
            "timestamp": time.time()
        })
        await prune_collection("pulse_tickets", limit=7)
        return True
    except:
        return False

async def run_pulse_agent(user_query):
    try:
        model = WatsonxChatModel(
            model_id="ibm/granite-3-8b-instruct",
            url=os.getenv("WATSONX_URL"),
            project_id=os.getenv("WATSONX_PROJECT_ID"),
            api_key=os.getenv("WATSONX_API_KEY"),
            parameters=ChatModelParameters(temperature=0)
        )

        messages = [
            SystemMessage("You are a risk analyst. Find risks and list them with clear titles."),
            UserMessage(user_query)
        ]

        response = await model.run(messages, tools=[search_docs])
        total_tokens = response.usage.total_tokens
        final_answer = response.get_text_content()

        risk_keywords = ["risk", "budget", "deficit", "failure", "threat", "danger"]
        if any(word in final_answer.lower() for word in risk_keywords):
            match = re.search(r'(?:Risk|Title):\s*(.*)', final_answer)
            ticket_title = match.group(1) if match else "Autonomously Detected Risk"
            await execute_ticket_creation(ticket_title)
            final_answer += "\n\n✅ [SYSTEM]: Risk detected and ticket sealed autonomously."

        energy, water = optimizer.calculate_metrics(total_tokens)
        
        client = DataAPIClient()
        db = client.get_database(os.getenv("ASTRA_DB_API_ENDPOINT"), token=os.getenv("ASTRA_DB_APPLICATION_TOKEN"))
        db.get_collection("ai_metrics").insert_one({
            "answer": final_answer,
            "tokens": total_tokens,
            "energy": energy,
            "water": water,
            "timestamp": time.time()
        })
        await prune_collection("ai_metrics", limit=7)
        
        if "sealed autonomously" in final_answer:
            notifier = PulseNotifier()
            await notifier.send_report_email(final_answer, water, energy)
        
        return {"answer": final_answer, "metrics": {"energy": energy, "water": water, "tokens": total_tokens}}

    except Exception as e:
        return {"answer": f"⚠️ System Error: {str(e)}", "metrics": None}