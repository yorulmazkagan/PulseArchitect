import os
from dotenv import load_dotenv
from astrapy import DataAPIClient

load_dotenv()

# .env'den bilgileri çekiyoruz
endpoint = os.getenv("ASTRA_DB_API_ENDPOINT")
token = os.getenv("ASTRA_DB_APPLICATION_TOKEN")

try:
    client = DataAPIClient()
    db = client.get_database(endpoint, token=token)
    print(f"\n✅ Astra DB Bağlantısı Başarılı!")
    print(f"🔗 Bağlanılan Veritabanı: {db.list_collection_names()}\n")
except Exception as e:
    print(f"\n❌ Bağlantı Hatası: {e}\n")