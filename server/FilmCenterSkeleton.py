import pickle
from typing import ByteString
from server.services.MovieService import MovieService

class FilmCenterSkeleton:

    async def search_movie(self, args_bytes: ByteString):
        try:
            busca = pickle.loads(args_bytes)
            if not isinstance(busca, str):
                raise ValueError("O parâmetro de busca deve ser uma string.")
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