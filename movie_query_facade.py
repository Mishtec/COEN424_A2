import json


class MovieQueryFacade:
    def __init__(self, db, redis_client):
        self.db = db
        self.redis_client = redis_client

    def query_top_n(self, top_n, from_year, to_year):
        # Check Redis for cached results
        redis_key = f'top-{top_n}-{from_year}-{to_year}'
        redis_results = self.redis_client.get(redis_key)

        if redis_results is not None:
            # If results exist in Redis, return them
            print("Fetch from Redis")
            return json.loads(redis_results)
        else:
            # If results do not exist in Redis, query MongoDB
            pipeline = [
                {"$match": {"year": {"$gte": from_year, "$lte": to_year}}},
                {"$sort": {"num_mflix_comments": -1}},
                {"$limit": top_n},
                {"$project": {"_id": 0, "title": "$title", "year": "$year", "num_comments": "$num_mflix_comments"}}
            ]

            results = list(self.db.movies.aggregate(pipeline))
            # print(results)

            if results:
                print("Insert to Redis")

                # Insert results into Redis for future retrieval in JSON format
                self.redis_client.set(redis_key, json.dumps(results, default=str))

                # Save results to MongoDB collection
                mongo_collection_name = f'top-{top_n}-{from_year}-{to_year}'
                self.db[mongo_collection_name].insert_many(results)

                # Return results
                return results
            else:
                # Handle MongoDB query: no results
                return {"error": "No results found"}
