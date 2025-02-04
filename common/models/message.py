from pydantic import BaseModel


class Message(BaseModel):
    type: int
    id: int
    obfReference: str
    methodId: str
    arguments: bytes

    class Config:
        arbitrary_types_allowed = True