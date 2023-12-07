import os
from pymongo import MongoClient
import redis
import json
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file if present

class MovieQueryFacade:
    def __init__(self):
        # Initialize MongoDB connection
        mongo_uri = os.getenv("MONGO_URI")
        self.mongo_client = MongoClient(mongo_uri)
        self.db = self.mongo_client[os.getenv("MONGO_DB")]

        # Initialize Redis connection
        redis_host = os.getenv("REDIS_HOST")
        redis_port = int(os.getenv("REDIS_PORT") 
        self.redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

    # def query_top_n(self, top_n, from_year, to_year):
  



