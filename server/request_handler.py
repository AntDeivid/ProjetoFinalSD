import json
from server.history_manager import HistoryManager
from server.FilmCenterDispatcher import FilmCenterDispatcher
from common.models.message import Message

class RequestHandler:
    def __init__(self):
        self.history = HistoryManager()
        self.dispatcher = FilmCenterDispatcher()

    async def processar_requisicao(self, mensagem_bytes):
        try:
            requisicao_dict = json.loads(mensagem_bytes.decode("utf-8"))  # Decodificar bytes para string antes de processar
            
            # Criar objeto Message a partir do dicionário
            requisicao = Message(**requisicao_dict)

            msg_id = requisicao.id

            resposta = self.history.buscar(msg_id)
            if resposta:
                print(f"Requisição duplicada detectada (ID: {msg_id}). Enviando resposta do cache.")
            else:
                resposta = await self.dispatcher.seleciona_esqueleto(requisicao)
                self.history.salvar(msg_id, resposta)

            return json.dumps(resposta).encode("utf-8")  # Certifique-se de enviar bytes de volta
        except Exception as e:
            print(f"Erro ao processar requisição: {e}")
            return json.dumps({"erro": str(e)}).encode("utf-8")