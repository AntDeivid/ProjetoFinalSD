import pickle
from typing import ByteString

from common.models.movie_list import MovieList
from server.services.MovieService import MovieService

class FilmCenterSkeleton:

    async def search_movie(self, args_bytes: ByteString):
        try:
            args = pickle.loads(args_bytes)
            if not isinstance(args, list) or not all(isinstance(arg, str) for arg in args):
                raise ValueError("Os parâmetros de busca devem ser uma lista de strings.")
            busca = args[0]
            filmes = await MovieService.search_movie(busca)
            return pickle.dumps(filmes)
        except ValueError as e:
            return pickle.dumps(e)
        except Exception as e:
            return pickle.dumps(e)

    async def get_streaming_options(self, args_bytes: ByteString):
        try:
            filme_id = pickle.loads(args_bytes)
            if not isinstance(filme_id, int):
                raise ValueError("O ID do filme deve ser um inteiro.")
            opcoes = await MovieService.get_streaming_options(filme_id)
            return pickle.dumps(opcoes)
        except ValueError as e:
            return pickle.dumps(e)
        except Exception as e:
            return pickle.dumps(e)

    async def create_movie_list(self, args_bytes: ByteString) -> MovieList:
        try:
            movie_list = pickle.loads(args_bytes)

            if not isinstance(movie_list, MovieList):
                raise ValueError("O objeto de lista de filmes é inválido.")

            result = await MovieService.create_movie_list(movie_list)
            return result
        except ValueError as e:
            raise e