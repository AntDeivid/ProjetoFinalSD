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
            args = pickle.loads(args_bytes)

            # Ajuste aqui: extraindo o ID do filme corretamente se vier como lista
            if not isinstance(args, list) or len(args) != 1 or not isinstance(args[0], int):
                raise ValueError("O ID do filme deve ser um inteiro.")

            filme_id = args[0]  # Pegando o ID correto

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
            return pickle.dumps(e)

    async def get_movies_by_ids(self, args_bytes: ByteString):
        try:
            movie_ids = pickle.loads(args_bytes)
            if not isinstance(movie_ids, list) or not all(isinstance(movie_id, int) for movie_id in movie_ids):
                raise ValueError("Os IDs dos filmes devem ser uma lista de inteiros.")
            filmes = await MovieService.get_movies_by_ids(movie_ids)
            return pickle.dumps(filmes)
        except ValueError as e:
            return pickle.dumps(e)
        except Exception as e:
            return pickle.dumps(e)