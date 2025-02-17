import socket
import threading
import asyncio
import pickle

from common.models.message import Message
from server.FilmCenterDispatcher import FilmCenterDispatcher


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


    async def tratar_requisicao(self, mensagem, endereco):
        try:
            requisicao = pickle.loads(mensagem) 
            resultado = await self.despachante.seleciona_esqueleto(requisicao)
            self.send_reply(pickle.dumps(resultado), endereco) 
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