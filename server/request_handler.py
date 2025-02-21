import json
from server.history_manager import HistoryManager
from server.FilmCenterDispatcher import FilmCenterDispatcher
from common.models.message import Message
import base64

class RequestHandler:
    def __init__(self):
        self.history = HistoryManager()
        self.dispatcher = FilmCenterDispatcher()

    async def processar_requisicao(self, mensagem_bytes):
        try:
            requisicao_dict = json.loads(mensagem_bytes.decode("utf-8"))  # Decodificar bytes para string antes de processar
            
            # Converte 'arguments' de Base64 de volta para bytes
            requisicao_dict["arguments"] = base64.b64decode(requisicao_dict["arguments"])

            # Criar objeto Message a partir do dicionário
            requisicao = Message(**requisicao_dict)

            msg_id = requisicao.id

            resposta = self.history.buscar(msg_id)
            print('resposta:', resposta)
            if resposta:
                print(f"Requisição duplicada detectada (ID: {msg_id}). Enviando resposta do cache.")
            else:
                resposta = await self.dispatcher.seleciona_esqueleto(requisicao)
                self.history.salvar(msg_id, resposta)

            # Converte 'arguments' para uma string Base64 antes de serializar
            resposta_dict = resposta.model_dump()
            resposta_dict["arguments"] = base64.b64encode(resposta_dict["arguments"]).decode("utf-8")

            return json.dumps(resposta_dict).encode("utf-8")
        except Exception as e:
            print(f"Erro ao processar requisição: {e}")
            return json.dumps({"erro": str(e)}).encode("utf-8")