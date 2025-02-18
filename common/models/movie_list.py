from typing import Optional

from pydantic import BaseModel

from common.models.movie import Movie


class  MovieList(BaseModel):
    id: Optional[int] = None
    user_id: int
    name: str
    description: str
    movies: Optional[list[Movie]] = None

    @property
    def movie_count(self):
        return len(self.movies)

    @property
    def better_rating(self):
        best_rating = 0
        best_movie = None
        for movie in self.movies:
            if movie.general_rating > best_rating:
                best_rating = movie.general_rating
                best_movie = movie
        return best_movie

    class Config:
        arbitrary_types_allowed = True