from pydantic import BaseModel


class Review(BaseModel):
    id: int
    movie_id: int
    user_id: int
    rating: float
    content: str

    class Config:
        arbitrary_types_allowed = True