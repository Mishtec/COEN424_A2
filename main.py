from movie_query_facade import MovieQueryFacade

def main():
    facade = MovieQueryFacade()
    result = facade.query_top_n(top_n=10, from_year=2000, to_year=2009)
    print(result)

if __name__ == "__main__":
    main()
