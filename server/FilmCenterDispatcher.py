import inspect
from typing import ByteString
from server.FilmCenterSkeleton import FilmCenterSkeleton

class FilmCenterDispatcher:
    async def seleciona_esqueleto(self, request):
        resposta = None
        try:
            # Encontra a classe dentro do módulo
            class_name = f"{request['object_reference']}Skeleton"
            obj_ref = globals()[class_name]

            method_name = request['method_id']
            print(f"Executando: {method_name}")
           
            # Obtém o método da classe
            method = getattr(obj_ref, method_name)

            # Verifica se o método existe e se espera um argumento do tipo ByteString
            if not callable(method):
                raise AttributeError(f"Método '{method_name}' não encontrado ou não é chamável.")
            
            signature = inspect.signature(method)
            if len(signature.parameters) != 2:
                raise TypeError(f"Método '{method_name}' deve ter exatamente dois parâmetros.")
            
            param_type = list(signature.parameters.values())[1].annotation
            if param_type is not ByteString:
                raise TypeError(f"O parâmetro do método '{method_name}' deve ser do tipo ByteString.")
            
            # Executa o método e obtem a resposta
            esqueleto = FilmCenterSkeleton()
            resposta = await method(esqueleto, request['arguments'])
            
        except ImportError as e:
            print(f"Erro ao importar módulo: {e}")
        except AttributeError as e:
            print(f"Erro ao acessar atributo ou classe: {e}")
        except TypeError as e:
            print(f"Erro de tipo: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")
        return resposta