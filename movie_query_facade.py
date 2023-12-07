import json
from db_init import initialize_database, initialize_redis


def parse_redis_string(redis_string):

    parsed_results = []
    for result in redis_string:
        movie_info = {
            "title": result.get("title", ""),
            "year": result.get("year", ""),
            "comments_count": result.get("num_mflix_comments", '')
        }
        parsed_results.append(movie_info)
    return parsed_results


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
            print("Fetch from Redis")
            return json.loads(redis_results)
        else:
            # If results do not exist in Redis, query MongoDB
            pipeline = [
                {"$match": {"year": {"$gte": from_year, "$lte": to_year}}},
                {"$sort": {"comments": -1}},
                {"$limit": top_n}
            ]

            results = list(self.db.movies.aggregate(pipeline))
            # print(results)

            if results:
                print("Insert to Redis")

                # Convert ObjectId to string for JSON serialization
                for result in results:
                    result["_id"] = str(result["_id"])

                results = parse_redis_string(results)

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
