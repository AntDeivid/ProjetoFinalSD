import socket

class UDPClient:
    def __init__(self, server_ip, server_port):
        self.server_address = (server_ip, server_port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_request(self, request_serializada):
        try:
            # Envia a mensagem já serializada ao servidor
            self.client_socket.sendto(request_serializada, self.server_address)
        except socket.error as e:
            print(f"Erro ao enviar a requisição: {e}")
    
    def get_response(self):
        try:
            # Recebe a resposta do servidor
            response_serializada, _ = self.client_socket.recvfrom(1024)
            return response_serializada
        except socket.error as e:
            print(f"Erro ao receber a resposta: {e}")
            return None

    def close(self):
        self.client_socket.close()
