from pydantic import BaseModel

from common.enums.streaming_option_id import StreamingOptionNameId


class StreamingOption(BaseModel):
    id: int
    name_id: StreamingOptionNameId
    url: str
    price: float
    free_trial: bool
    free_trial_duration: int

    class Config:
        arbitrary_types_allowed = True
