import pytest
from api.api_manager import ApiManager
from constants import NAME, PASSWORD
from utils.data_generator import DataGenerator


@pytest.mark.api
class TestMoviesAPI:

    @pytest.mark.parametrize("page, pageSize", [
        (1, 10),
        (1, 1),
        (2, 5)
    ])
    def test_get_movies_list_positive(self, api_manager: ApiManager, page: int, pageSize: int):
        """Позитив: Получить список фильмов с пагинацией """
        result = api_manager.movies_api.get_movies(page=page, pageSize=pageSize)

        assert result['status_code'] == 200
        data = result['data']
        assert 'movies' in data
        assert len(data['movies']) == pageSize

    @pytest.mark.parametrize("genreId", [i for i in range(1, 11)])  # Список из 10 жанров
    def test_movies_filter_by_genre(self, api_manager: ApiManager, genreId: int):
        """Позитив: API возвращает список фильмов с определёнными жанрами"""
        result = api_manager.movies_api.get_movies(genreId=genreId)

        assert result['status_code'] == 200
        data = result['data']
        assert 'movies' in data

    @pytest.mark.parametrize("page, pageSize, genreId", [
        (0, 10, 1),
        (1, 0, 2),
        (1, 10, 0),
        ("test", 10, 1),
        (1, "test", 2),
        (1, 10, "test")
    ])
    def test_movies_invalid_pagination(self, api_manager: ApiManager, page, pageSize, genreId):
        """Негатив: Неверные параметры - API возвращает 400"""
        result = api_manager.movies_api.get_movies(page=page, pageSize=pageSize, genreId=genreId)

        # API правильно возвращает 400 для невалидных параметров
        assert result['status_code'] == 400

    def test_movies_response_structure(self, api_manager: ApiManager):
        """Проверка обязательной структуры ответа"""
        result = api_manager.movies_api.get_movies()

        assert result['status_code'] == 200
        data = result['data']
        assert all(key in data for key in ['movies', 'count', "page", "pageSize", "pageCount"])

        required_fields = ['id', 'name', "description", 'genreId', 'price', "rating", 'published', 'genre']
        for movie in data['movies']:
            assert all(field in movie for field in required_fields)
            assert 'name' in movie['genre']

    def test_create_movies(self, api_manager: ApiManager):
        """Позитив: Создание фильма """
        api_manager.auth_api.authenticate(user_creds=(NAME, PASSWORD))

        response =  api_manager.movies_api.create_movie({
            "name": DataGenerator.generate_random_movie_name(),
            "imageUrl": "https://poknok.art/uploads/posts/2022-11/thumbs/1668713844_33-poknok-art-p-ptitsi-belom-fone-foto-35.png",
            "price": DataGenerator.generate_random_int(99, 1000),
            "description": DataGenerator.generate_random_text(),
            "location": DataGenerator.generate_random_choice(['MSK', 'SPB']),
            "published": DataGenerator.generate_random_bool(),
            "genreId": api_manager.movies_api.genre_id(),
        }, expected_status=201)

        assert 'id' in response.json()


    def test_patch_movies(self, api_manager: ApiManager, random_movie):
        """Позитив: Редактирование фильма """

        movie = random_movie
        movie_id = movie['id']

        result = api_manager.movies_api.patch_movies({
            "name": DataGenerator.generate_random_movie_name(),
            "imageUrl": "https://poknok.art/uploads/posts/2022-11/thumbs/1668713844_33-poknok-art-p-ptitsi-belom-fone-foto-35.png",
            "price": DataGenerator.generate_random_int(99, 1000),
            "description": DataGenerator.generate_random_text(),
            "location": DataGenerator.generate_random_choice(['MSK', 'SPB']),
            "published": DataGenerator.generate_random_bool(),
            "genreId": api_manager.movies_api.genre_id(),
        }, expected_status=200, id = movie_id)

        assert result['status_code'] == 200



    def test_create_reviews(self, api_manager: ApiManager, random_movie):
        """Позитив: создание, получение, редактирование, удаление ревью"""
        # Получаем id нового фильма
        movie = random_movie
        movie_id = int(movie['id'])
        # Создаём отзыв
        result = api_manager.movies_api.create_reviews(id=movie_id, rating = 4, text = "Хорошее кино")
        assert result['status_code'] == 201
        # Получаем этот отзыв
        result = api_manager.movies_api.get_reviews(id=movie_id)
        assert result['status_code'] == 200
        # Редактируем отзыв
        result = api_manager.movies_api.put_reviews(id=movie_id, rating = 3, text = "Хорошее кино, но...")
        assert result['status_code'] == 200
        # Удаляем отзыв
        result = api_manager.movies_api.delete_reviews(id=movie_id)
        assert result['status_code'] == 200

    def test_delete_movies(self, api_manager: ApiManager, random_movie):
        """Позитив: Удаление фильма """

        movie = random_movie
        movie_id = int(movie['id'])

        result = api_manager.movies_api.delete_movies(id=movie_id)
        assert result['status_code'] == 200

    def test_create_genre(self, api_manager: ApiManager):
        api_manager.auth_api.authenticate(user_creds=(NAME, PASSWORD))
        # Создание нового жанра
        result = api_manager.movies_api.create_genre(name="Test_genreуee")
        assert result['status_code'] == 201
        # Получение id жанра
        id = result['data']['id']
        result = api_manager.movies_api.get_genre(id=id)
        assert result['status_code'] == 200
        # Удаление жанра по id
        result = api_manager.movies_api.delete_genre(id=id)
        assert result['status_code'] == 200