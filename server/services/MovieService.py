from typing import List, Optional

from common.models.movie import Movie
from common.models.streaming_option import StreamingOption
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
        pass

    @classmethod
    async def create_movie_list(cls, user_id: int, name: str, description: str, movie_ids: List[int]) -> str:
        pass