import json
from typing import ByteString
from common.models.movie_list import MovieList
from server.services.MovieService import MovieService

class FilmCenterSkeleton:

    async def search_movie(self, args_bytes: ByteString):
        try:
            args_json = args_bytes.decode("utf-8")
            args = json.loads(args_json)
            
            if not isinstance(args, list) or not all(isinstance(arg, str) for arg in args):
                raise ValueError("Os parâmetros de busca devem ser uma lista de strings.")
            busca = args[0]
            filmes = await MovieService.search_movie(busca)
            return json.dumps(filmes).encode("utf-8")
        except ValueError as e:
            return json.dumps(e).encode("utf-8")
        except Exception as e:
            return json.dumps(e).encode("utf-8")

    async def get_streaming_options(self, args_bytes: ByteString):
        try:
            args_json = args_bytes.decode("utf-8")
            args = json.loads(args_json)

            if not isinstance(args, list) or len(args) != 1 or not isinstance(args[0], int):
                raise ValueError("O ID do filme deve ser um inteiro.")

            filme_id = args[0]

            opcoes = await MovieService.get_streaming_options(filme_id)
            return json.dumps(opcoes).encode("utf-8")

        except ValueError as e:
            return json.dumps(e).encode("utf-8")
        except Exception as e:
            return json.dumps(e).encode("utf-8")

    async def create_movie_list(self, args_bytes: ByteString):
        try:
            args_json = args_bytes.decode("utf-8")
            movie_list_json = json.loads(args_json)
            movie_list = MovieList(**movie_list_json)

            if not isinstance(movie_list, MovieList):
                raise ValueError("O objeto de lista de filmes é inválido.")

            result = await MovieService.create_movie_list(movie_list)
            return json.dumps(result).encode("utf-8")
        except ValueError as e:
            return json.dumps(e).encode("utf-8")

    async def get_movies_by_ids(self, args_bytes: ByteString):
        try:
            args_json = args_bytes.decode("utf-8")
            movie_ids = json.loads(args_json)

            if not isinstance(movie_ids, list) or not all(isinstance(movie_id, int) for movie_id in movie_ids):
                raise ValueError("Os IDs dos filmes devem ser uma lista de inteiros.")
            filmes = await MovieService.get_movies_by_ids(movie_ids)
            return json.dumps(filmes).encode("utf-8")
        except ValueError as e:
            return json.dumps(e).encode("utf-8")
        except Exception as e:
            return json.dumps(e).encode("utf-8")