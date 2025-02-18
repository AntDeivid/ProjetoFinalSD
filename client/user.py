from client.proxy import FilmeProxy
from InquirerPy import prompt
from client.UDPClient import UDPClient
from typing import List
from common.models.movie import Movie
from common.models.movie_list import MovieList
from common.models.streaming_option import StreamingOption
from json import loads

class FilmeClient:
    def __init__(self, proxy):
        self.proxy = proxy

    def buscar_filme(self):
        query = prompt([
            {
                "type": "input",
                "name": "query",
                "message": "Digite o nome do filme para buscar:",
            }
        ])["query"]

        try:
            response: List[Movie] = self.proxy.buscar_filme(query)
            
            if not response:
                print("Erro: Nenhuma resposta recebida do servidor.")
                return

            print("\nInformações do filme:")
            print(response)
        except Exception as e:
            print(f"Erro: {e}")

    def buscar_streaming(self):
        filme_id = prompt([
            {
                "type": "input",
                "name": "filme_id",
                "message": "Digite o ID do filme:",
            }
        ])["filme_id"]

        response = self.proxy.buscar_streaming(filme_id)
        if "error" in response:
            print(f"Erro: {response['error']}")
        else:
            print("\nOpções de Streaming disponíveis:")
            for option in response:
                print(f"- Plataforma: {option['plataforma']}, Link: {option['link']}")

    def criar_lista(self):
        nome_lista = prompt([
            {
                "type": "input",
                "name": "nome_lista",
                "message": "Digite o nome da lista:",
            }
        ])["nome_lista"]

        user_id = prompt([
            {
                "type": "input",
                "name": "user_id",
                "message": "Digite o ID do usuário:",
            }
        ])["user_id"]

        description = prompt([
            {
                "type": "input",
                "name": "description",
                "message": "Digite a descrição da lista:",
            }
        ])["description"]

        filmes = prompt([
            {
                "type": "input",
                "name": "filmes",
                "message": "Digite os IDs dos filmes (separados por vírgula):",
            }
        ])["filmes"].split(",")

        movie_list = MovieList(
            user_id=int(user_id),
            name=nome_lista,
            description=description,
        )

        response = self.proxy.criar_lista(movie_list, filmes)
        if "error" in response:
            print(f"Erro: {response['error']}")
        else:
            print("\nMensagem do servidor:")
            print(response)

    def menu(self):
        while True:
            # Opções de menu usando InquirerPy
            action = prompt([
                {
                    "type": "list",
                    "name": "menu",
                    "message": "Escolha uma operação:",
                    "choices": [
                        "1 - Buscar Filme",
                        "2 - Buscar Opções de Streaming",
                        "3 - Criar Lista de Filmes",
                        "0 - Sair",
                    ],
                }
            ])["menu"]

            if action.startswith("1"):
                self.buscar_filme()
            elif action.startswith("2"):
                self.buscar_streaming()
            elif action.startswith("3"):
                self.criar_lista()
            elif action.startswith("0"):
                print("Encerrando cliente...")
                break


if __name__ == "__main__":
    # Configurações do servidor
    SERVER_IP = "127.0.0.1"
    SERVER_PORT = 7896

    client = UDPClient(SERVER_IP, SERVER_PORT)
    proxy = FilmeProxy(client)
    filme_client = FilmeClient(proxy)

    try:
        filme_client.menu()
    finally:    
        proxy.limpar_historico()
        client.close()
