import unittest
import json
import time
import numpy as np
from unittest.mock import MagicMock, patch
from movie_query_facade import MovieQueryFacade

class TestMovieQueryFacade(unittest.TestCase):

    def setUp(self):
        # Create a mock for the database
        self.mock_db = MagicMock()

        # Create a mock for the Redis client
        self.mock_redis_client = MagicMock()

        # Replace the actual initialize_database and initialize_redis functions with mocks
        with patch('your_module.initialize_database', return_value=self.mock_db):
            with patch('your_module.initialize_redis', return_value=self.mock_redis_client):
                # Create an instance of MovieQueryFacade for testing
                self.movie_query_facade = MovieQueryFacade()

    def measure_response_time(self, func, *args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        response_time = end_time - start_time
        return result, response_time

    def measure_deletion_time(self, func, *args, **kwargs):
        # Measure the deletion time exclusively
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        deletion_time = end_time - start_time
        return result, deletion_time

    def test_query_top_n_from_mongodb_with_empty_redis(self):
        # Given: Redis returns None (empty cache)
        self.mock_redis_client.get.return_value = None

        # And: MongoDB returns some results
        expected_results = [{"title": f"Movie{i}", "year": 2010, "num_comments": 100 + i} for i in range(1, 6)]
        self.mock_db.movies.aggregate.return_value = expected_results

        # When: The query_top_n method is called 100 times
        response_times = []
        deletion_times = []
        for _ in range(100):
            # Measure the query response time
            _, response_time = self.measure_response_time(self.movie_query_facade.query_top_n, 5, 2000, 2022)
            response_times.append(response_time)

            # Measure the deletion time (exclusive to the query time)
            _, deletion_time = self.measure_deletion_time(self.mock_redis_client.delete, 'your_key')
            deletion_times.append(deletion_time)

        # Then: Results are fetched from MongoDB, inserted into Redis, and returned
        average_response_time = np.mean(response_times)
        percentile_50th = np.percentile(response_times, 50)
        percentile_90th = np.percentile(response_times, 90)

        print(f"Case (1) - Query:")
        print(f"Average Response Time: {average_response_time:.4f} seconds")
        print(f"50th Percentile Response Time: {percentile_50th:.4f} seconds")
        print(f"90th Percentile Response Time: {percentile_90th:.4f} seconds")

        average_deletion_time = np.mean(deletion_times)
        print(f"Average Deletion Time: {average_deletion_time:.4f} seconds")

        self.assertEqual(len(response_times), 100)
        self.mock_redis_client.set.assert_called_once()
        self.mock_db.movies.insert_many.assert_called_once()

        # Reset the call counts for the next iteration
        self.mock_redis_client.set.reset_mock()
        self.mock_db.movies.insert_many.reset_mock()

    def test_query_top_n_from_redis_with_filled_cache(self):
        # Given: Redis returns some cached results
        expected_results = [{"title": f"Movie{i}", "year": 2010, "num_comments": 100 + i} for i in range(1, 6)]
        self.mock_redis_client.get.return_value = json.dumps(expected_results)

        # When: The query_top_n method is called 100 times
        response_times = []
        for _ in range(100):
            # Measure the query response time
            _, response_time = self.measure_response_time(self.movie_query_facade.query_top_n, 5, 2000, 2022)
            response_times.append(response_time)

            # Deletion time will be zero since no deletion is performed

        # Then: Results are fetched from Redis
        average_response_time = np.mean(response_times)
        percentile_50th = np.percentile(response_times, 50)
        percentile_90th = np.percentile(response_times, 90)

        print(f"Case (2) - Query:")
        print(f"Average Response Time: {average_response_time:.4f} seconds")
        print(f"50th Percentile Response Time: {percentile_50th:.4f} seconds")
        print(f"90th Percentile Response Time: {percentile_90th:.4f} seconds")

        self.mock_db.movies.aggregate.assert_not_called()  # MongoDB should not be queried
        self.mock_redis_client.set.assert_not_called()  # Redis should not be updated

if __name__ == '__main__':
    unittest.main()
