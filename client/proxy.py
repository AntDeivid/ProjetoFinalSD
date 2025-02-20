from typing import List
from client.UDPClient import UDPClient
from common.models.message import Message
import json
from common.models.movie import Movie
from common.models.movie_list import MovieList

class FilmeProxy:
    def __init__(self):
        self.client = UDPClient()
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
            arguments=json.dumps(args).encode("utf-8") 
        )

        self.client.send_request(message)
        resposta_message: Message = self.client.get_response()

        if resposta_message is None:
            raise Exception("Erro ao receber resposta do servidor.")

        return resposta_message

    def buscar_filme(self, query) -> List[Movie]:
        try:
            response_message: Message = self.do_operation("FilmCenter", "search_movie", [query])
            if not isinstance(response_message, Message):
                raise TypeError("Resposta não é do tipo Message")

            response_data = json.loads(response_message.arguments.decode("utf-8"))
            if isinstance(response_data, list):
                return [Movie(**movie) if isinstance(movie, dict) else movie for movie in response_data]
            else:
                raise TypeError("Resposta não é uma lista de filmes")

        except Exception as e:
            raise e

    def criar_lista(self, movie_list: MovieList, movie_ids=List) -> Movie:
        movies_ids_integer = [int(movie_id) for movie_id in movie_ids]
        try:
            response_message: Message = self.do_operation("FilmCenter", "get_movies_by_ids", movies_ids_integer)
            print("pegou os filmes")
            if not isinstance(response_message, Message):
                raise TypeError("Resposta não é do tipo Message")
            response = json.loads(response_message.arguments.decode("utf-8"))
            movie_list.movies = response
            print("setou os filmes")
        except Exception as e:
            raise e

        try:
            response_message: Message = self.do_operation("FilmCenter", "create_movie_list", movie_list.model_dump())
            print("criou a lista")
            if not isinstance(response_message, Message):
                raise TypeError("Resposta não é do tipo Message")

            response = json.loads(response_message.arguments.decode("utf-8"))
            return response
        except Exception as e:
            raise e
        
    def buscar_streaming(self, filme_id) -> list:
        try:
            response_message: Message = self.do_operation("FilmCenter", "get_streaming_options", [filme_id])
            if not isinstance(response_message, Message):
                return {"error": "Resposta inválida do servidor."}

            response = json.loads(response_message.arguments.decode("utf-8"))
            return response
            
        except Exception as e:
            return {"error": f"Erro ao buscar streaming: {str(e)}"}
        
    
    def limpar_historico(self):
        self.do_operation("Server", "clear_history", [])

    def close(self):
        self.client.close()