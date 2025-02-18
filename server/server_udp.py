import socket
import asyncio
import pickle
import csv
import os
import signal
import sys
import ast

from server.FilmCenterDispatcher import FilmCenterDispatcher

class UDPServer:
    def __init__(self, host='127.0.0.1', port=7896, historico_file="server/data/historico.csv"):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65535)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65535)
        self.socket.bind((self.host, self.port))
        self.despachante = FilmCenterDispatcher()
        self.historico_file = historico_file

        self._criar_pasta_data()
        self._criar_csv()

        # Capturar sinais de encerramento (CTRL+C ou SIGTERM)
        signal.signal(signal.SIGINT, self.limpar_servidor)
        signal.signal(signal.SIGTERM, self.limpar_servidor)

        print(f"Servidor UDP rodando em {self.host}:{self.port}")

    def _criar_pasta_data(self):
        pasta_data = os.path.dirname(self.historico_file)
        if not os.path.exists(pasta_data):
            os.makedirs(pasta_data)

    def _criar_csv(self):
        if not os.path.exists(self.historico_file):
            with open(self.historico_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["id", "resposta"])

    def limpar_servidor(self, *args):
        print("\n[INFO] Encerrando servidor.")
        sys.exit(0)

    def get_request(self):
        mensagem, endereco = self.socket.recvfrom(8192)
        return mensagem, endereco

    def send_reply(self, resposta, endereco):
        self.socket.sendto(resposta, endereco)

    def buscar_no_historico(self, msg_id):
        try:
            with open(self.historico_file, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader, None) 
                for row in reader:
                    if row and int(row[0]) == msg_id: 
                        return pickle.loads(ast.literal_eval(row[1]))
        except FileNotFoundError:
            print(f"Arquivo de histórico não encontrado: {self.historico_file}")
            return None
        except Exception as e:
            print(f"Erro ao ler o histórico: {e}")
            return None
        return None

    def salvar_no_historico(self, msg_id, resposta):
        with open(self.historico_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([msg_id, repr(pickle.dumps(resposta))])

    async def tratar_requisicao(self, mensagem, endereco):
        try:
            requisicao = pickle.loads(mensagem)
            msg_id = requisicao.id

            if requisicao.methodId == "clear_history":
                self.limpar_historico()
                resposta = {"status": "OK", "message": "Histórico limpo"}
            else:
                resposta = self.buscar_no_historico(msg_id)
                if resposta:
                    print(f"Mensagem duplicada detectada (ID: {msg_id})! Retornando resposta do cache.")
                else:
                    resultado = await self.despachante.seleciona_esqueleto(requisicao)
                    resposta = resultado
                    self.salvar_no_historico(msg_id, resposta)

            self.send_reply(pickle.dumps(resposta), endereco)
        except Exception as e:
            print(f"Erro ao processar requisição: {e}")

    def limpar_historico(self):
        print("[INFO] Limpeza do histórico solicitada.")
        if os.path.exists(self.historico_file):
            os.remove(self.historico_file)

    def iniciar(self):
        loop = asyncio.get_event_loop()
        while True:
            mensagem, endereco = self.get_request()
            loop.run_until_complete(self.tratar_requisicao(mensagem, endereco))

if __name__ == "__main__":
    servidor = UDPServer()
    servidor.iniciar()