from client.UDPClient import UDPClient
import pickle

class Mensagem:
    def __init__(self, object_ref, method, args):
        self.object_ref = object_ref
        self.method = method
        self.args = args

    def serializar(self):
        return pickle.dumps({
            "object_ref": self.object_ref,
            "method": self.method,
            "args": self.args
        })

    @staticmethod
    def desserializar(data):
        obj = pickle.loads(data)
        return Mensagem(obj["object_ref"], obj["method"], obj["args"])

class FilmeProxy:
    def __init__(self, client):
        self.client = client

    def do_operation(self, object_ref, method, args):
        mensagem = Mensagem(object_ref, method, args)
        mensagem_serializada = mensagem.serializar()
        
        resposta_serializada = self.client.send_request(mensagem_serializada)
        if resposta_serializada is None:
            raise Exception("Erro ao receber resposta do servidor.")
        
        resposta_mensagem = Mensagem.desserializar(resposta_serializada)
        return resposta_mensagem.args 

    def buscar_filme(self, query):
        return self.do_operation("Locadora", "buscarFilme", [query])

    def buscar_streaming(self, filme_id):
        return self.do_operation("Locadora", "buscarStreaming", [filme_id])

    def criar_lista(self, nome_lista, filmes):
        return self.do_operation("Locadora", "criarLista", [nome_lista, filmes])
