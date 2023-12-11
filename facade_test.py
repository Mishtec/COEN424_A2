import unittest
import time
import numpy as np
import matplotlib.pyplot as plt


class FacadeTest(unittest.TestCase):

    def __init__(self, db, redis_client, facade):
        super().__init__()
        self.db = db
        self.redis_client = redis_client
        self.movie_query_facade = facade

    def measure_performance(self, top_n, from_year, to_year, iterations):
        query_times = []
        deletion_times = []

        for _ in range(iterations):
            # Measure the time taken for the query
            start_query_time = time.time()
            self.redis_client.delete(f'top-{top_n}-{from_year}-{to_year}')  # Delete Redis record
            self.movie_query_facade.query_top_n(top_n, from_year, to_year)
            end_query_time = time.time()
            query_times.append(end_query_time - start_query_time)

            # Measure the time taken for deletion
            start_deletion_time = time.time()
            self.redis_client.delete(f'top-{top_n}-{from_year}-{to_year}')  # Delete Redis record again
            end_deletion_time = time.time()
            deletion_times.append(end_deletion_time - start_deletion_time)
            print(query_times)
            print(deletion_times)

        return query_times, deletion_times


if __name__ == '__main__':
    # Run the tests
    unittest.main()
