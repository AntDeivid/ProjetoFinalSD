from pydantic import BaseModel

from common.models.streaming_option import StreamingOption


class Movie(BaseModel):
    id: int
    title: str
    year: int
    rating: float
    runtime: int
    genre: str
    description: str
    actors: str
    director: str
    writer: str
    streaming_options: list[StreamingOption]

    class Config:
        arbitrary_types_allowed = True