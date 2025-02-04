from client.UDPClient import UDPClient
from common.models.message import Message
import pickle

METHOD_IDS = {
    "search_movie": 1,
    "buscarStreaming": 2,
    "criarLista": 3
}

class FilmeProxy:
    def __init__(self, client: UDPClient):
        self.client = client

    def do_operation(self, object_ref, method, args):
        if method not in METHOD_IDS:
            raise ValueError(f"Método desconhecido: {method}")

        message = Message(
            type=0,
            id=1, 
            obfReference=object_ref,
            methodId=METHOD_IDS[method],
            arguments=pickle.dumps(args)
        )
        print(f"Enviando requisição: {message}")

        message_serializada = pickle.dumps(message)
        
        resposta_serializada = self.client.send_request(message_serializada)

        if resposta_serializada is None:
            raise Exception("Erro ao receber resposta do servidor.")

        print(f"Resposta bruta recebida: {resposta_serializada}")
        
        resposta_message = pickle.loads(resposta_serializada)

        # Certifique-se de que 'resposta_message' contém um atributo válido
        if not hasattr(resposta_message, 'resultado'):
            raise Exception("Resposta do servidor não contém o atributo 'resultado'")

        return resposta_message.resultado


    def buscar_filme(self, query):
        return self.do_operation("MovieService", "search_movie", [query])

    # def buscar_streaming(self, filme_id):
    #     return self.do_operation("Locadora", 2, [filme_id])  # O método "buscarStreaming" tem ID 2

    # def criar_lista(self, nome_lista, filmes):
    #     return self.do_operation("Locadora", 3, [nome_lista, filmes])  # O método "criarLista" tem ID 3
