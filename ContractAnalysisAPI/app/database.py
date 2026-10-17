from pymongo import MongoClient
from app.config import MONGODB_URI

client = MongoClient(MONGODB_URI)
db= client.get_database("mydb")

# we are writing the collections here
contracts_collection = db["contracts"]
analysis_collection =  db["analysis"]

try:
    analysis_collection.drop_index("analysis_id_1")
    print("Successfully dropped obsolete analysis_id_1 index!")
except Exception as e:
    print(f"Index already dropped or not found: {e}")

def init_db():
    contracts_collection.create_index("contract_id", unique = True)
    