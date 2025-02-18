from client.UDPClient import UDPClient
from common.models.message import Message
import pickle
from common.models.movie import Movie

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

    def limpar_historico(self):
        self.do_operation("Server", "clear_history", [])

