import socket
import asyncio
from server.request_handler import RequestHandler

class UDPServer:
    def __init__(self, host='127.0.0.1', port=7896):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))
        self.request_handler = RequestHandler()

    async def iniciar(self):
        print(f"Servidor UDP rodando em {self.host}:{self.port}")
        while True:
            mensagem, endereco = self.socket.recvfrom(8192)
            resposta = await self.request_handler.processar_requisicao(mensagem)

            # Para testar o timeout e reenvio, descomente a linha abaixo e faça uma requisição para o servidor pelo cliente
            # continue

            self.socket.sendto(resposta, endereco)

if __name__ == "__main__":
    servidor = UDPServer()
    asyncio.run(servidor.iniciar())