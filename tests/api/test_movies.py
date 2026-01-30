import pytest
from api.api_manager import ApiManager


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
