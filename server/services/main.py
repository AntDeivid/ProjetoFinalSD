import asyncio

from server.services.TMDbService import TMDbService


async def test_search_movies():
    query = "Inception"
    movies = await TMDbService.search_movie(query)

    print(f"Resultados para '{query}':")
    for movie in movies:
        print(f"- {movie.title} ({movie.year}) - Nota: {movie.vote_average}")


if __name__ == "__main__":
    asyncio.run(test_search_movies())
