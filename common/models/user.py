from pydantic import BaseModel

from common.models.review import Review


class User(BaseModel):
    id: int
    username: str
    email: str
    password: str
    reviews: list[Review]

    class Config:
        arbitrary_types_allowed = True