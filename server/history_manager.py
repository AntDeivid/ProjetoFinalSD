import csv
import os
import json
import base64

class HistoryManager:
    def __init__(self, historico_file="server/data/historico.csv"):
        self.historico_file = historico_file
        self._criar_pasta_data()
        self._criar_csv()

    def _criar_pasta_data(self):
        pasta_data = os.path.dirname(self.historico_file)
        if not os.path.exists(pasta_data):
            os.makedirs(pasta_data)

    def _criar_csv(self):
        if not os.path.exists(self.historico_file):
            with open(self.historico_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["id", "resposta"])

    def buscar(self, msg_id):
        try:
            with open(self.historico_file, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader, None)  # Pula o cabeçalho
                for row in reader:
                    if row and int(row[0]) == msg_id:
                        resposta_dict = json.loads(row[1])
                        resposta_dict["arguments"] = base64.b64decode(resposta_dict["arguments"])
                        return Message(**resposta_dict)
        except FileNotFoundError:
            print(f"[ERRO] Arquivo de histórico não encontrado: {self.historico_file}")
        except Exception as e:
            print(f"[ERRO] Falha ao buscar no histórico: {e}")
        return None

    def salvar(self, msg_id, resposta):
        try:
            resposta_dict = resposta.model_dump()
            resposta_dict["arguments"] = base64.b64encode(resposta_dict["arguments"]).decode("utf-8")
            with open(self.historico_file, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([msg_id, json.dumps(resposta_dict)])
        except Exception as e:
            print(f"[ERRO] Falha ao salvar no histórico: {e}")

    def limpar(self):
        print("[INFO] Limpando histórico de requisições...")
        if os.path.exists(self.historico_file):
            os.remove(self.historico_file)
            self._criar_csv()