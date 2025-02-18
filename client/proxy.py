from client.UDPClient import UDPClient
from common.models.message import Message
import pickle

from common.models.movie import Movie


class FilmeProxy:
    def __init__(self, client: UDPClient):
        self.client = client

    def do_operation(self, object_ref, method, args) -> Message:
        message = Message(
            type=0,
            id=1,
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
        
    def buscar_streaming(self, filme_id) -> list:
        try:
            response_message: Message = self.do_operation("FilmCenter", "get_streaming_options", [filme_id])
            if not isinstance(response_message, Message):
                return {"error": "Resposta inválida do servidor."}

            response = pickle.loads(response_message.arguments)
            return response
            
        except Exception as e:
            return {"error": f"Erro ao buscar streaming: {str(e)}"}
