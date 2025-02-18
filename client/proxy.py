from typing import Optional, List

from client.UDPClient import UDPClient
from common.models.message import Message
import pickle
from common.models.movie import Movie
from common.models.movie_list import MovieList

class FilmeProxy:
    def __init__(self, client: UDPClient):
        self.client = client
        self.message_id = 0  

    def get_next_id(self):
        self.message_id += 1
        return self.message_id

    def do_operation(self, object_ref, method, args) -> Message:
        message = Message(
            type=0,
            id=self.get_next_id(),  
            obfReference=object_ref,
            methodId=method,
            arguments=pickle.dumps(args)
        )

        self.client.send_request(message)
        resposta_message: Message = self.client.get_response()

        if resposta_message is None:
            raise Exception("Erro ao receber resposta do servidor.")

        return resposta_message

    def buscar_filme(self, query) -> Movie:
        try:
            response_message: Message = self.do_operation("FilmCenter", "search_movie", [query])
            if not isinstance(response_message, Message):
                raise TypeError("Resposta não é do tipo Message")

            response = pickle.loads(response_message.arguments)
            return response

        except Exception as e:
            raise e

    def criar_lista(self, movie_list: MovieList, movie_ids=List) -> Movie:
        movies_ids_integer = [int(movie_id) for movie_id in movie_ids]
        try:
            response_message: Message = self.do_operation("FilmCenter", "get_movies_by_ids", movies_ids_integer)
            print("pegou os filmes")
            if not isinstance(response_message, Message):
                raise TypeError("Resposta não é do tipo Message")
            response = pickle.loads(response_message.arguments)
            movie_list.movies = response
            print("setou os filmes")
        except Exception as e:
            raise e

        try:
            response_message: Message = self.do_operation("FilmCenter", "create_movie_list", movie_list)
            print("criou a lista")
            if not isinstance(response_message, Message):
                raise TypeError("Resposta não é do tipo Message")

            response = pickle.loads(response_message.arguments)
            return response
        except Exception as e:
            raise e
        
    def buscar_streaming(self, filme_id) -> list:
        try:
            response_message: Message = self.do_operation("FilmCenter", "get_streaming_options", [filme_id])
            if not isinstance(response_message, Message):
                return {"error": "Resposta inválida do servidor."}

            response = pickle.loads(response_message.arguments)
            return response
            
        except Exception as e:
            return {"error": f"Erro ao buscar streaming: {str(e)}"}
        
    
    def limpar_historico(self):
        self.do_operation("Server", "clear_history", [])