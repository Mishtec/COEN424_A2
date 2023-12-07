import json
import os
from pymongo import MongoClient
import redis
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file


def initialize_database():
    # Initialize MongoDB connection
    mongo_uri = os.getenv("MONGODB_URI")
    mongo_db_name = os.getenv("MONGO_DB")

    # Print for debugging
    # print(f"MONGODB_URI: {mongo_uri}")
    # print(f"MONGO_DB value: {mongo_db_name}")

    # Connect to MongoDB
    client = MongoClient(mongo_uri)

    try:
        # Ping MongoDB server
        response = client.server_info()
        print("Connected to MongoDB. Server info:", response)
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")

    # Access the specified database
    db = client[mongo_db_name]
    return db


def initialize_redis():
    # Initialize Redis connection
    redis_host = os.getenv("REDIS_HOST")
    redis_port = int(os.getenv("REDIS_PORT"))
    redis_password = os.getenv("REDIS_PASSWORD")
    redis_client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
    # print(f"REDIS_HOST: {os.getenv('REDIS_HOST')}")
    # print(f"REDIS_PORT: {os.getenv('REDIS_PORT')}")
    # print(f"REDIS_PASSWORD: {os.getenv('REDIS_PASSWORD')}")

    # Check the connection using the ping command
    try:
        response = redis_client.ping()
        if response:
            print("Connected to Redis. Ping response:", response)
        else:
            print("Failed to connect to Redis.")
    except Exception as e:
        print(f"Error connecting to Redis: {e}")

    return redis_client


if __name__ == "__main__":
    # Example usage to test initialization
    db = initialize_database()
    redis_client = initialize_redis()

    print("Database and Redis initialized!")
