from client.UDPClient import UDPClient
from common.models.message import Message
import pickle

from common.models.movie import Movie


class FilmeProxy:
    def __init__(self, client: UDPClient):
        self.client = client

    def do_operation(self, object_ref, method, args) -> Message:  # Retorna Message
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

        return resposta_message  # Retorna o objeto Message sem desserializar arguments

    def buscar_filme(self, query):
        response: Message = self.do_operation("FilmCenter", "search_movie", [query])
        return pickle.loads(response.arguments)  # Desserializa arguments aqui
    # def buscar_streaming(self, filme_id):
    #     return self.do_operation("Locadora", 2, [filme_id])  # O método "buscarStreaming" tem ID 2

    # def criar_lista(self, nome_lista, filmes):
    #     return self.do_operation("Locadora", 3, [nome_lista, filmes])  # O método "criarLista" tem ID 3