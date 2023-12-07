import json
from db_init import initialize_database, initialize_redis


class MovieQueryFacade:
    def __init__(self):
        # Initialize MongoDB connection
        self.db = initialize_database()

        # Initialize Redis connection
        self.redis_client = initialize_redis()

    def query_top_n(self, top_n, from_year, to_year):
        # Check Redis for cached results
        redis_key = f'top-{top_n}-{from_year}-{to_year}'
        redis_results = self.redis_client.get(redis_key)

        if redis_results is not None:
            # If results exist in Redis, return them
            return json.loads(redis_results)
        else:
            # If results do not exist in Redis, query MongoDB
            pipeline = [
                {"$match": {"year": {"$gte": from_year, "$lte": to_year}}},
                {"$sort": {"comments": -1}},
                {"$limit": top_n},
                {"$project": {"_id": 0, "name": 1, "year": 1, "comments": 1}}
            ]

            results = list(self.db.movies.aggregate(pipeline))
            # print(results)

            if results:
                # Insert results into Redis for future retrieval in JSON format
                self.redis_client.set(redis_key, json.dumps(results))

                # Save results to MongoDB collection
                mongo_collection_name = f'top-{top_n}-{from_year}-{to_year}'
                self.db[mongo_collection_name].insert_many(results)

                # Return results
                return json.dumps(results, indent=2)
            else:
                # Handle the case where MongoDB query returned no results
                return json.dumps({"error": "No results found"}, indent=2)
