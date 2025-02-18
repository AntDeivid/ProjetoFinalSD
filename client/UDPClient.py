import pickle
import socket

from common.models.message import Message

class UDPClient:
    def __init__(self, server_ip, server_port, timeout=2, max_retries=3):
        self.server_address = (server_ip, server_port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65535)
        self.client_socket.settimeout(timeout)
        self.max_retries = max_retries

    def send_request(self, request: Message):
        try:
            # Serializa a mensagem antes de enviar
            request_serializada = pickle.dumps(request)
            self.client_socket.sendto(request_serializada, self.server_address)
        except socket.error as e:
            print(f"Erro ao enviar requisição: {e}")
            return None

    def get_response(self) -> Message | None:
        retries = 0
        while retries < self.max_retries:
            try:
                response_serializada, _ = self.client_socket.recvfrom(65535)
                response: Message = pickle.loads(response_serializada)
                return response
            except socket.timeout:
                retries += 1
                print(f"Timeout: tentando novamente ({retries}/{self.max_retries})")
            except socket.error as e:
                print(f"Erro ao receber resposta: {e}")
                return None

        print("Número máximo de tentativas excedido.")
        return None
   

    def close(self):
        self.client_socket.close()

