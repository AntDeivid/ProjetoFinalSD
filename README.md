# Central de Filmes - Sistemas Distribuídos

## Descrição

Este projeto consiste em um serviço remoto, a "Central de Filmes", que permite aos usuários pesquisar informações sobre filmes, encontrar opções de streaming e criar listas personalizadas de filmes. Ele foi desenvolvido como parte da disciplina de Sistemas Distribuídos (2024.2).

## Funcionalidades Principais

*   **Pesquisa de Filmes:** Busca informações sobre filmes com base em um termo de pesquisa.
*   **Opções de Streaming:** Obtém as opções de streaming disponíveis para um filme específico.
*   **Criação de Listas:** Permite aos usuários criar e gerenciar listas personalizadas de filmes.

## Arquitetura

A aplicação é construída utilizando uma arquitetura distribuída que envolve os seguintes componentes:

*   **Cliente:** Interface do usuário para interagir com o serviço remoto.
*   **Servidor:** Hospeda os serviços remotos e a lógica de negócios.
*   **FilmCenter (Serviço Remoto):** Fornece as funcionalidades principais da Central de Filmes.
*   **TMDbService:** Interage com a API do TMDb (The Movie Database) para obter informações sobre filmes.
*   **Comunicação:** Utiliza o protocolo UDP para comunicação entre cliente e servidor.
*   **Formato de Dados:** JSON é usado para a serialização e desserialização de dados.

## Métodos Remotos

*   **`buscar_filme(query: string) -> Movie`:**
    *   Pesquisa um filme com base em um termo de busca.
    *   Retorna um objeto `Movie` contendo informações do filme.
    *   Lança exceções em caso de filme não encontrado ou parâmetros inválidos.

*   **`buscar_streaming(filme_id: int) -> list`:**
    *   Obtém as opções de streaming disponíveis para um filme específico.
    *   Retorna uma lista de opções de streaming.
    *   Lança exceções em caso de filme não disponível em streaming ou parâmetro inválido.

*   **`criar_lista(movie_list: MovieList, movie_ids: List[int]) -> MovieList`:**
    *   Cria uma nova lista de filmes no servidor.
    *   Retorna um objeto `MovieList` representando a lista criada.
    *   Lança exceções em caso de parâmetros inválidos.

## Classes Implementadas

*   **Message:** Estrutura fundamental para a comunicação remota.
*   **UdpClient:** Responsável pelo envio e recebimento de mensagens UDP.
*   **Dispatcher:** Direciona as requisições aos serviços apropriados no servidor.
*   **Skeleton:** Implementa a lógica do serviço no servidor.
*   **Proxy:** Atua como intermediário no cliente.
*   **TMDbService:** Interage com a API do TMDb.
*   **Movie:** Representa um filme.
*   **User:** Representa um usuário.
*   **StreamingOption:** Representa uma opção de streaming.
*   **MovieList:** Representa uma lista de filmes.
*   **Review:** Representa uma avaliação de um filme.

## Tratamento de Falhas

*   **Mensagens Duplicadas:** O servidor detecta e ignora mensagens duplicadas usando um histórico armazenado em arquivo CSV.
*   **Erros no Despachante:** O Despachante trata erros como `ImportError`, `AttributeError`, `TypeError` e `Exception` ao encaminhar requisições.

## Alterações Propostas Pelo Professor

*   **Remoção de Rede no User:** As funções relacionadas à rede foram retiradas da classe `User` e distribuídas entre as classes `Proxy` e `UdpClient`.
*   **Correção do Tratamento de Mensagens Duplicadas:** A lógica de retorno da resposta para o cliente foi corrigida para garantir o correto funcionamento do tratamento de mensagens duplicadas.
*   **Implementação de Retransmissão (Timeout):** Implementado um mecanismo de retransmissão com timeout para lidar com a perda de mensagens.

## Como Executar

1.  Clone o repositório.
2.  Configure as dependências necessárias (ex: bibliotecas Python).
3.  Execute o servidor:
    ```bash
    python server_udp.py
    ```
4.  Execute o cliente:
    ```bash
    python user.py
    ```

## Demonstração

Link para o vídeo demonstrando as funcionalidades e tratamento de falhas:

[https://www.youtube.com/watch?v=6Cm1_QSd37g](https://www.youtube.com/watch?v=6Cm1_QSd37g)

## Equipe

*   Jeferson Aires de Sousa
*   Antonio Deivid Santos Costa
*   Kaynan Pereira de Sousa
*   Victor Emanuel de Sousa Costa