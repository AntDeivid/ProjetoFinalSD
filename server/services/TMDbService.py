from typing import Optional, List

import httpx

from common.models.movie import Movie


class TMDbService:
    BASE_URL = "https://api.themoviedb.org/3"
    API_KEY = "04ed3e8e1846a1f7cfc65756040cb0f2"

    @classmethod
    async def search_movie(cls, query: str, year: Optional[int] = None) -> List[Movie]:
        url = f"{cls.BASE_URL}/search/movie"
        params = {
            "api_key": cls.API_KEY,
            "query": query,
            "language": "pt-BR"
        }
        if year:
            params["year"] = year

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            data = response.json()

        return [cls._format_movie(movie) for movie in data.get("results", [])]

    @classmethod
    def _format_movie(cls, data: dict) -> Movie:
        return Movie(
            id=data["id"],
            title=data["title"],
            year=int(data.get("release_date", "0000")[:4]) if data.get("release_date") else 0,
            runtime=data.get("runtime", 0),
            genre=", ".join([g["name"] for g in data.get("genres", [])]),
            description=data.get("overview", ""),
            actors="",
            director="",
            writer="",
            streaming_options=[],
            reviews=[],
            poster_url=f"https://image.tmdb.org/t/p/w500{data.get('poster_path', '')}",
            backdrop_url=f"https://image.tmdb.org/t/p/w780{data.get('backdrop_path', '')}",
            trailer_url=cls._extract_trailer_url(data.get("videos", {}).get("results", [])),
            language=data.get("original_language", ""),
            popularity=data.get("popularity", 0.0),
            vote_average=data.get("vote_average", 0.0),
        )

    @classmethod
    def _extract_trailer_url(cls, videos: List[dict]) -> str:
        for video in videos:
            if video.get("type") == "Trailer" and video.get("site") == "YouTube":
                return f"https://www.youtube.com/watch?v={video.get('key', '')}"
        return ""