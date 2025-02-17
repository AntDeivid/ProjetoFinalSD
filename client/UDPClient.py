import pickle
import socket

from common.models.message import Message

class UDPClient:
    def __init__(self, server_ip, server_port):
        self.server_address = (server_ip, server_port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_request(self, request: Message):
        try:
            # Serializa a mensagem antes de enviar
            request_serializada = pickle.dumps(request)
            self.client_socket.sendto(request_serializada, self.server_address)
        except socket.error as e:
            print(f"Erro ao enviar requisição: {e}")
            return None

    def get_response(self) -> Message | None:
        try:
            response_serializada, _ = self.client_socket.recvfrom(65535)
            response: Message = pickle.loads(response_serializada)
            return response
        except socket.error as e:
            print(f"Erro ao receber resposta: {e}")
            return None
   

    def close(self):
        self.client_socket.close()

