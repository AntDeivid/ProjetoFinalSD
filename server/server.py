import socket
import threading
import asyncio
from server.FilmCenterDispatcher import FilmCenterDispatcher
import pickle

class UDPServer:
    def __init__(self, host='127.0.0.1', port=7896):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))
        self.despachante = FilmCenterDispatcher()
        print(f"Servidor UDP rodando em {self.host}:{self.port}")

    def get_request(self):
        mensagem, endereco = self.socket.recvfrom(1024)
        return mensagem, endereco

    def send_reply(self, resposta, endereco):
        self.socket.sendto(resposta, endereco)

    def desempacota_requisicao(self, array):
        return pickle.loads(array)

    def empacota_resposta(self, resultado, request_id):
        return pickle.dumps({"request_id": request_id, "resultado": resultado})

    async def tratar_requisicao(self, mensagem, endereco):
        try:
            requisicao = self.desempacota_requisicao(mensagem)
            resultado = await self.despachante.seleciona_esqueleto(requisicao)
            resposta = self.empacota_resposta(resultado, requisicao['request_id'])
            self.send_reply(resposta, endereco)
        except Exception as e:
            print(f"Erro ao processar requisição: {e}")

    def iniciar(self):
        loop = asyncio.get_event_loop()
        while True:
            mensagem, endereco = self.get_request()
            loop.run_until_complete(self.tratar_requisicao(mensagem, endereco))

if __name__ == "__main__":
    servidor = UDPServer()
    servidor.iniciar()