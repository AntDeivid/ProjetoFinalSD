import csv
import os
import json
from typing import List
from common.models.movie_list import MovieList
from common.models.movie import Movie
from common.enums.streaming_option_id import StreamingOptionNameId
from common.models.review import Review
from common.models.streaming_option import StreamingOption


CSV_FILE = "server/data/movieList.csv"

CSV_SO = "server/data/streamingOptions.csv"

def save_movie_list(movie_list: MovieList):
    """Salva um único MovieList no arquivo CSV."""
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["id", "user_id", "name", "description", "movies"])  # Cabeçalho
        writer.writerow([
            movie_list.id,
            movie_list.user_id,
            movie_list.name,
            movie_list.description,
            json.dumps([
                movie.model_dump(by_alias=True, exclude_none=True) for movie in movie_list.movies
            ])  # Convertemos a lista de filmes para JSON com exclusão de none
        ])
    print(f"MovieList salva em '{CSV_FILE}' com sucesso!")

def load_movie_lists() -> List[MovieList]:
    """Carrega a lista de MovieList do arquivo CSV."""
    movie_lists = []
    if not os.path.exists(CSV_FILE):
        print(f"Arquivo '{CSV_FILE}' não encontrado. Criando um novo.")
        return movie_lists

    with open(CSV_FILE, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            movies_data = json.loads(row['movies'])
            movies = [Movie(**data) for data in movies_data]  # Criamos objetos Movie a partir do JSON

            movie_list = MovieList(
                id=int(row['id']),
                user_id=int(row['user_id']),
                name=row['name'],
                description=row['description'],
                movies=movies
            )
            movie_lists.append(movie_list)
    print(f"Lista de MovieLists carregada de '{CSV_FILE}' com sucesso!")
    return movie_lists

def update_movie_list(list_id: int, new_data: dict):
    """Atualiza um MovieList na lista e no CSV."""
    movie_lists = load_movie_lists()
    for movie_list in movie_lists:
        if movie_list.id == list_id:
            # Atualizar os atributos básicos da MovieList
            for key, value in new_data.items():
                if hasattr(movie_list, key):
                    setattr(movie_list, key, value)
            save_movie_list(movie_list)
            print(f"MovieList com id '{list_id}' atualizada.")
            return
    print(f"MovieList com id '{list_id}' não encontrada.")

def delete_movie_list(list_id: int):
    """Deleta um MovieList da lista e do CSV."""
    movie_lists = load_movie_lists()
    movie_lists = [movie_list for movie_list in movie_lists if movie_list.id != list_id]
    for movie_list in movie_lists:
        save_movie_list(movie_list)
    print(f"MovieList com id '{list_id}' deletada.")

def get_streaming_options(movie_id: int) -> List[StreamingOption]:
    """Percorre o CSV procurando as opções de streaming de um filme específico."""
    streaming_options = []
    if not os.path.exists(CSV_SO):
        print(f"Arquivo '{CSV_SO}' não encontrado. Criando um novo.")
        # Cria o arquivo CSV se ele não existir
        with open(CSV_SO, 'w', newline='', encoding='utf-8') as csvfile:
             writer = csv.writer(csvfile)
             writer.writerow(["id", "name_id", "url", "price", "free_trial", "free_trial_duration", "movie_id"]) # Cabeçalho
             print(f"Arquivo '{CSV_SO}' criado com sucesso!")
        return streaming_options # Retorna vazio para não tentar ler o arquivo vazio

    with open(CSV_SO, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if int(row['movie_id']) == movie_id:
                streaming_option = StreamingOption(
                    id=int(row['id']),
                    name_id=StreamingOptionNameId(row['name_id']),
                    url=row['url'],
                    price=float(row['price']),
                    free_trial=bool(row['free_trial']),
                    free_trial_duration=int(row['free_trial_duration']),
                    movie_id=int(row['movie_id'])
                )
                streaming_options.append(streaming_option)
    print(f"Opções de streaming para o filme com id '{movie_id}' carregadas de '{CSV_SO}' com sucesso!")
    return streaming_options

def save_streaming_options(streaming_options: List[StreamingOption]):
    """Salva as opções de streaming no arquivo CSV."""
    with open(CSV_SO, 'a', newline='', encoding='utf-8') as csvfile:  # Abre no modo 'a' (append)
        writer = csv.writer(csvfile)
        if os.path.getsize(CSV_SO) == 0: # Se o arquivo estiver vazio, escreve o cabeçalho.
          writer.writerow(["id", "name_id", "url", "price", "free_trial", "free_trial_duration", "movie_id"])

        for option in streaming_options:
            writer.writerow([
                option.id,
                option.name_id.value,
                option.url,
                option.price,
                option.free_trial,
                option.free_trial_duration,
                option.movie_id
            ])
    print(f"Opções de streaming salvas em '{CSV_SO}' com sucesso!")

if __name__ == '__main__':
    # Criação de objetos de exemplo
    review1 = Review(id=1, movie_id=1, user_id=1, rating=5.0, content="Excelente filme!")
    review2 = Review(id=2, movie_id=1, user_id=2, rating=4.5, content=None)
    review3 = Review(id=3, movie_id=2, user_id=3, rating=2.0, content="Mais ou menos...")
    review4 = Review(id=4, movie_id=3, user_id=1, rating=3.0, content="É legalzinho.")

    streaming1 = StreamingOption(id=1, name_id=StreamingOptionNameId.NETFLIX, url="netflix.com/filme1", price=10.0,
                                free_trial=True, free_trial_duration=7, movie_id=1)
    streaming2 = StreamingOption(id=2, name_id=StreamingOptionNameId.AMAZON_PRIME, url="amazon.com/filme1", price=8.0,
                                free_trial=False, free_trial_duration=0, movie_id=1)
    streaming3 = StreamingOption(id=3, name_id=StreamingOptionNameId.DISNEY_PLUS, url="disneyplus.com/filme2", price=12.0,
                                free_trial=True, free_trial_duration=14, movie_id=2)
    streaming4 = StreamingOption(id=4, name_id=StreamingOptionNameId.HULU, url="hulu.com/filme3", price=9.0,
                                free_trial=False, free_trial_duration=0, movie_id=3)
    streaming5 = StreamingOption(id=5, name_id=StreamingOptionNameId.APPLE_TV, url="appletv.com/filme1", price=11.0,
                                free_trial=True, free_trial_duration=30, movie_id=1) # filme 1 com mais um streaming

    movie1 = Movie(
        id=1, title="O Poderoso Chefão", year=1972, runtime=175, genre="Crime",
        description="A saga da família Corleone.", actors="Marlon Brando, Al Pacino",
        director="Francis Ford Coppola", writer="Mario Puzo",
        poster_url="url_poster1", backdrop_url="url_backdrop1",
        trailer_url="url_trailer1", language="en", popularity=8.8, vote_average=9.2,
        streaming_options=[streaming1, streaming2, streaming5], reviews=[review1, review2] # filme 1 em 3 plataformas
    )
    movie2 = Movie(
        id=2, title="Interestelar", year=2014, runtime=169, genre="Ficção Científica",
        description="Uma equipe de exploradores viaja através de um buraco de minhoca.",
        actors="Matthew McConaughey, Anne Hathaway", director="Christopher Nolan",
        writer="Jonathan Nolan", poster_url="url_poster2", backdrop_url="url_backdrop2",
        trailer_url="url_trailer2", language="en", popularity=8.6, vote_average=8.6,
        streaming_options=[streaming3], reviews=[review3]
    )
    movie3 = Movie(
        id=3, title="A Chegada", year=2016, runtime=116, genre="Ficção Científica",
        description="Uma linguista é recrutada para se comunicar com extraterrestres.",
        actors="Amy Adams, Jeremy Renner", director="Denis Villeneuve",
        writer="Eric Heisserer", poster_url="url_poster3", backdrop_url="url_backdrop3",
        trailer_url="url_trailer3", language="pt", popularity=7.9, vote_average=7.7,
        streaming_options=[streaming4], reviews=[review4]
    )

    movie_list1 = MovieList(
        id=1, user_id=10, name="Favoritos do João", description="Filmes que o João mais gosta.",
        movies=[movie1, movie2, movie3]
    )
    movie_list2 = MovieList(
        id=2, user_id=20, name="Séries da Maria", description="Séries que a Maria está assistindo.",
        movies=[]
    )
    initial_movie_lists = [movie_list1, movie_list2]
    save_movie_list(initial_movie_lists)

    # Carregar as listas do CSV
    loaded_lists = load_movie_lists()

    all_streaming_options = []
    for movie_list in loaded_lists:
      for movie in movie_list.movies:
        all_streaming_options.extend(movie.streaming_options)
    # Salva as opções de streaming no CSV
    save_streaming_options(all_streaming_options)


    # Teste do get_streaming_options:
    movie_id_to_search = 1
    streaming_options = get_streaming_options(movie_id_to_search)
    print(f"\nOpções de streaming para o filme com id {movie_id_to_search}:")
    for option in streaming_options:
      print(f'- {option.name_id}: {option.url}, Preço: {option.price}')
    
    movie_id_to_search = 2
    streaming_options = get_streaming_options(movie_id_to_search)
    print(f"\nOpções de streaming para o filme com id {movie_id_to_search}:")
    for option in streaming_options:
      print(f'- {option.name_id}: {option.url}, Preço: {option.price}')

    movie_id_to_search = 3
    streaming_options = get_streaming_options(movie_id_to_search)
    print(f"\nOpções de streaming para o filme com id {movie_id_to_search}:")
    for option in streaming_options:
      print(f'- {option.name_id}: {option.url}, Preço: {option.price}')