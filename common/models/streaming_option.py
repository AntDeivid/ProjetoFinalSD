from pydantic import BaseModel

from common.enums.streaming_option_id import StreamingOptionNameId


class StreamingOption(BaseModel):
    id: int
    name_id: StreamingOptionNameId
    url: str
    price: float
    free_trial: bool
    free_trial_duration: int
    movie_id: str

    class Config:
        arbitrary_types_allowed = True
