from client.UDPClient import UDPClient
from common.models.message import Message
import pickle


class FilmeProxy:
    def __init__(self, client: UDPClient):
        self.client = client

    def do_operation(self, object_ref, method, args):
        message = Message(
            type=0,  # Supondo que 0 seja um tipo padrão para requisições
            id=1,  # Pode ser um identificador único para cada requisição
            obfReference=object_ref,
            methodId=method,  # Deve ser string, como "search_movie"
            arguments=pickle.dumps(args)  # Serializa os argumentos corretamente
        )

        message_serializada = pickle.dumps(message)
        resposta_serializada = self.client.send_request(message_serializada)

        if resposta_serializada is None:
            raise Exception("Erro ao receber resposta do servidor.")
        
        resposta_message = pickle.loads(resposta_serializada)
        return pickle.loads(resposta_message['resultado'])  # Desserializa o resultado

    def buscar_filme(self, query):
        return self.do_operation("MovieService", "search_movie", [query])

    # def buscar_streaming(self, filme_id):
    #     return self.do_operation("Locadora", 2, [filme_id])  # O método "buscarStreaming" tem ID 2

    # def criar_lista(self, nome_lista, filmes):
    #     return self.do_operation("Locadora", 3, [nome_lista, filmes])  # O método "criarLista" tem ID 3
