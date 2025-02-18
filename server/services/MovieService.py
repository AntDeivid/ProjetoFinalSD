from typing import List, Optional

from common.models.movie import Movie
from common.models.movie_list import MovieList
from common.models.streaming_option import StreamingOption
from server.services.CSVService import get_streaming_options, save_movie_list
from server.services.TMDbService import TMDbService


class MovieService:
    @classmethod
    async def search_movie(cls, query: str, year: Optional[int] = None) -> List[Movie]:
        movies = await TMDbService.search_movie(query, year)
        if not movies:
            raise ValueError("No movies found")
        return movies

    @classmethod
    async def get_streaming_options(cls, movie_id: str) -> List[StreamingOption]:
        streaming_options = get_streaming_options(movie_id)
        if not streaming_options:
            raise ValueError("No streaming options found")
        return streaming_options

    @classmethod
    async def create_movie_list(cls, movie_list: MovieList) -> MovieList:
        save_movie_list(movie_list)
        return movie_list
