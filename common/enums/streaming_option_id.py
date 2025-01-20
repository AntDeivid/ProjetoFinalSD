from enum import Enum


class StreamingOptionNameId(str, Enum):
    NETFLIX = "Netflix"
    HULU = "Hulu"
    AMAZON_PRIME = "Amazon Prime"
    DISNEY_PLUS = "Disney Plus"
    HBO_MAX = "HBO Max"
    APPLE_TV = "Apple TV"
    YOUTUBE = "YouTube"
    GOOGLE_PLAY = "Google Play"
    VUDU = "Vudu"
    CRUNCHYROLL = "Crunchyroll"
    FUNIMATION = "Funimation"
    PEACOCK = "Peacock"