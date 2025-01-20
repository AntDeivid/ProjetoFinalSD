from pydantic import BaseModel

from common.models.review import Review
from common.models.streaming_option import StreamingOption


class Movie(BaseModel):
    id: int
    title: str
    year: int
    runtime: int
    genre: str
    description: str
    actors: str
    director: str
    writer: str
    streaming_options: list[StreamingOption]
    reviews: list[Review]

    @property
    def general_rating(self):
        total = 0
        for review in self.reviews:
            total += review.rating
        return total / len(self.reviews)

    class Config:
        arbitrary_types_allowed = True