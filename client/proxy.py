from client.UDPClient import UDPClient
import json

class Mensagem:
    def __init__(self, object_ref, method, args):
        self.object_ref = object_ref
        self.method = method
        self.args = args

    def serializar(self):
        return json.dumps(self.__dict__).encode()

    @staticmethod
    def desserializar(data):
        obj = json.loads(data.decode())
        return Mensagem(obj["object_ref"], obj["method"], obj["args"])


class FilmeProxy:
    def __init__(self, client):
        self.client = client

    def do_operation(self, object_ref, method, args):
        # Monta a mensagem com os parâmetros
        mensagem = Mensagem(object_ref, method, args)
        mensagem_serializada = mensagem.serializar()
        
        # Envia a mensagem pelo cliente UDP e espera a resposta
        resposta_serializada = self.client.send_request(mensagem_serializada)
        
        # Desserializa a resposta recebida
        if resposta_serializada is None:
            raise Exception("Erro ao receber resposta do servidor.")
        
        resposta_mensagem = Mensagem.desserializar(resposta_serializada)
        return resposta_mensagem.args  # O resultado está nos argumentos da resposta

    def buscar_filme(self, query):
        return self.do_operation("Locadora", "buscarFilme", [query])

    def buscar_streaming(self, filme_id):
        return self.do_operation("Locadora", "buscarStreaming", [filme_id])

    def criar_lista(self, nome_lista, filmes):
        return self.do_operation("Locadora", "criarLista", [nome_lista, filmes])
