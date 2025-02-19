import pickle
from server.history_manager import HistoryManager
from server.FilmCenterDispatcher import FilmCenterDispatcher
from common.models.message import Message

class RequestHandler:
    def __init__(self):
        self.history = HistoryManager()
        self.dispatcher = FilmCenterDispatcher()

    async def processar_requisicao(self, mensagem_bytes):
        try:
            requisicao = pickle.loads(mensagem_bytes)
            msg_id = requisicao.id

            resposta = self.history.buscar(msg_id)
            if resposta:
                print(f"Requisição duplicada detectada (ID: {msg_id}). Enviando resposta do cache.")
            else:
                resposta = await self.dispatcher.seleciona_esqueleto(requisicao)
                self.history.salvar(msg_id, resposta)

            return pickle.dumps(resposta)
        except Exception as e:
            print(f"Erro ao processar requisição: {e}")
            return pickle.dumps({"erro": str(e)})