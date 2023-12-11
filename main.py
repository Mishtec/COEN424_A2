from movie_query_facade import MovieQueryFacade
from facade_test import FacadeTest
from db_init import initialize_database, initialize_redis


def query():
    top_n = int(input("Enter Top-N: "))
    from_year = int(input("Enter From Year: "))
    to_year = int(input("Enter To Year: "))
    return top_n, from_year, to_year


def main():
    # Initialize database and Redis
    db = initialize_database()
    redis_client = initialize_redis()

    # Query instance
    facade = MovieQueryFacade(db, redis_client)
    facade_test = FacadeTest(db, redis_client, facade)

    while True:
        print("Options:")
        print("1. Query Top-N Movies")
        print("2. Test 50th Percentile Query Performance")
        print("3. Test 90th Percentile Query Performance")
        print("4. Quit")

        choice = input("Enter your choice (1 ,2, 3, or '4' to Quit): \n")

        if choice == '4':
            print("Quit...")
            break
        elif choice == '1':
            top_n, from_year, to_year = query()
            result = facade.query_top_n(top_n, from_year, to_year)
            print(result)
        elif choice == '2':
            iterations = int(input("Enter iterations: "))
            top_n, from_year, to_year = query()
            facade_test.measure_performance(top_n, from_year, to_year, iterations)
            # facade_test.test_50th_percentile_query_performance(top_n, from_year, to_year, iterations)
        elif choice == '3':
            iterations = int(input("Enter iterations: "))
            top_n, from_year, to_year = query()
            # facade_test.test_90th_percentile_query_performance(top_n, from_year, to_year, iterations)
        else:
            print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":
    main()
