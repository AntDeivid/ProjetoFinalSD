import socket
import json
import threading
import pandas as pd
import os

class ServicoExemplo:
    def soma(self, a, b):
        return a + b

class Server:
    def __init__(self, host="127.0.0.1", porta=5000, historico_file="historico_de_respostas.csv"):
        self.host = host
        self.porta = porta
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.porta))
        self.historico_file = historico_file

        if not os.path.exists(self.historico_file):
            df = pd.DataFrame(columns=["id", "servico", "metodo", "argumentos", "resposta"])
            df.to_csv(self.historico_file, index=False)

    def carregar_historico(self):
        return pd.read_csv(self.historico_file) if os.path.exists(self.historico_file) else pd.DataFrame()

    def salvar_historico(self, id_requisicao, servico, metodo, argumentos, resposta):
        df = pd.DataFrame([{
            "id": id_requisicao,
            "servico": servico,
            "metodo": metodo,
            "argumentos": json.dumps(argumentos),  
            "resposta": json.dumps(resposta)
        }])
        df.to_csv(self.historico_file, mode='a', header=False, index=False)

    def get_request(self):
        mensagem, endereco = self.socket.recvfrom(1024)
        return mensagem, endereco

    def send_reply(self, resposta, endereco):
        self.socket.sendto(resposta.encode(), endereco)

    def tratar_requisicao(self, mensagem, endereco):
        try:
            dados = json.loads(mensagem.decode())
            id_requisicao = dados["id"]
            servico = dados["servico"]
            metodo = dados["metodo"]
            argumentos = dados["argumentos"]

            df_historico = self.carregar_historico()
            resposta_existente = df_historico[df_historico["id"] == str(id_requisicao)]  

            if not resposta_existente.empty:
                resposta = json.loads(resposta_existente.iloc[0]["resposta"])  
            else:
                objeto = globals()[servico]()  
                metodo_chamado = getattr(objeto, metodo)
                resposta = metodo_chamado(*argumentos)

                self.salvar_historico(id_requisicao, servico, metodo, argumentos, resposta)

            resposta_json = json.dumps({"id": id_requisicao, "resposta": resposta})
            self.send_reply(resposta_json, endereco)

        except Exception as e:
            print(f"Erro no servidor: {e}")

    def iniciar(self):
        print(f"Servidor UDP rodando em {self.host}:{self.porta}")
        while True:
            mensagem, endereco = self.get_request()
            threading.Thread(target=self.tratar_requisicao, args=(mensagem, endereco)).start()

if __name__ == "__main__":
    servidor = Server()
    servidor.iniciar()
