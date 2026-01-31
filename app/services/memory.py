import os
from dotenv import load_dotenv
from astrapy import DataAPIClient
from pathlib import Path

load_dotenv()

ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
COLLECTION_NAME = "pulse_docs" 

def store_in_memory():
    md_path = Path("data/output_report.md")
    if not md_path.exists():
        print("❌ Error: perception.py must be run first, Markdown not found!")
        return

    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    chunks = content.split("## ")
    documents = []
    for i, chunk in enumerate(chunks):
        if chunk.strip():
            documents.append({
                "_id": f"chunk_{i}",
                "text": "## " + chunk,
                "metadata": {"source": "strategic_report_2026.pdf"}
            })

    print(f"🧠 {len(documents)} The data packet is ready to be sent to Astra DB.")

    try:
        client = DataAPIClient()
        db = client.get_database(ENDPOINT, token=TOKEN)
        
        if COLLECTION_NAME not in db.list_collection_names():
            collection = db.create_collection(COLLECTION_NAME)
        else:
            collection = db.get_collection(COLLECTION_NAME)
        
        collection.delete_many({}) 
        collection.insert_many(documents)

        print(f"✅ Success! {len(documents)} the part was embedded in the memory (Astra DB).")
        print(f"🔗 Colleciton: {COLLECTION_NAME}")

    except Exception as e:
        print(f"❌ Memory Error: {e}")

if __name__ == "__main__":
    store_in_memory()