import inspect
import json
from typing import ByteString

from common.models.message import Message
from server.FilmCenterSkeleton import FilmCenterSkeleton
from server.history_manager import HistoryManager

history = HistoryManager()
class FilmCenterDispatcher:
    async def seleciona_esqueleto(self, request: Message) -> Message:
        try:
            if(request.methodId == "clear_history"):
                history.limpar()
                 
            
            class_name = f"{request.obfReference}Skeleton"
            obj_ref = globals()[class_name]

            method_name = request.methodId
            print(f"Executando: {method_name}")

            method = getattr(obj_ref, method_name)

            if not callable(method):
                raise AttributeError(f"Método '{method_name}' não encontrado ou não é chamável.")

            signature = inspect.signature(method)
            if len(signature.parameters) != 2:
                raise TypeError(f"Método '{method_name}' deve ter exatamente dois parâmetros.")

            param_type = list(signature.parameters.values())[1].annotation
            if param_type is not ByteString:
                raise TypeError(f"O parâmetro do método '{method_name}' deve ser do tipo ByteString.")

            esqueleto = obj_ref()
            resposta = await method(esqueleto, request.arguments)

            response_message = Message(
                type=1,
                id=request.id,
                obfReference=request.obfReference,
                methodId=request.methodId,
                arguments=resposta
            )

        except ImportError as e:
            print(f"Erro ao importar módulo: {e}")
            response_message = Message(
                type=1,
                id=request.id,
                obfReference=request.obfReference,
                methodId=request.methodId,
                arguments=json.dumps(str(e)).encode("utf-8")
            )
        except AttributeError as e:
            print(f"Erro ao acessar atributo ou classe: {e}")
            response_message = Message(
                type=1,
                id=request.id,
                obfReference=request.obfReference,
                methodId=request.methodId,
                arguments=json.dumps(str(e)).encode("utf-8")
            )
        except TypeError as e:
            print(f"Erro de tipo: {e}")
            response_message = Message(
                type=1,
                id=request.id,
                obfReference=request.obfReference,
                methodId=request.methodId,
                arguments=json.dumps(str(e)).encode("utf-8")
            )
        except Exception as e:
            print(f"Erro inesperado: {e}")
            response_message = Message(
                type=1,
                id=request.id,
                obfReference=request.obfReference,
                methodId=request.methodId,
                arguments=json.dumps(str(e)).encode("utf-8")
            )
        return response_message