import os

from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from config import VECTOR_DB_NAME, VECTOR_COLLECTION_NAME


class MongoDBConnector:

    uri = None
    client = None

    def __init__(self):
        load_dotenv()

        self.uri = os.getenv("DB_URL").replace("<db_username>", os.getenv("DB_USERNAME")).replace("<db_password>", os.getenv("DB_PASSWORD"))
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))

    def ping(self):
        # Send a ping to confirm a successful connection
        self.client.admin.command('ping')

    def get_vector_collection(self):
        try:
            return self.client.get_database(VECTOR_DB_NAME).get_collection(VECTOR_COLLECTION_NAME)
        except Exception as e:
            print(e)

    def get_vector_chunks(self, query, embedding_model):
        query_vector = embedding_model.embed_query(query)
        return self.get_vector_collection().aggregate([
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "embedding",
                    "queryVector": query_vector,
                    "numCandidates": 100,
                    "limit": 100
                }
            },
            {
                "$sort": {
                    "timestamp": -1
                }
            }
        ])