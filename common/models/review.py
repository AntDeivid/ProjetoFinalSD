from pydantic import BaseModel
from typing import Optional


class Review(BaseModel):
    id: int
    movie_id: int
    user_id: int
    rating: float
    content: Optional[str] = None
    class Config:
        arbitrary_types_allowed = True