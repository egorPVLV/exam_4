import pytest
import string
import random
#тест


class TestMoviesAPI:
    @pytest.fixture
    def random_string(self):
        """Генератор случайных строк"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=20))


    @pytest.mark.api
    @pytest.mark.parametrize("page, limit", [
        (1, 10),
        (1, 1),
        (2, 5)
    ])
    def test_get_movies_list_positive(self, api_manager, page, limit):
        """Позитив: Получить список фильмов с пагинацией (API игнорирует limit)"""
        result = api_manager.movies_api.get_movies(page=page, limit=limit)

        assert result['status_code'] == 200
        data = result['data']
        assert 'movies' in data
        assert isinstance(data['count'], int)
        # API всегда возвращает 10 фильмов, игнорируя limit
        assert len(data['movies']) == 10

    @pytest.mark.api
    @pytest.mark.parametrize("genre", ["Анимация", "Комедия", "Драма", "Мюзикл"])
    def test_movies_filter_by_genre(self, api_manager, genre):
        """Позитив: API возвращает любые фильмы при любом жанре"""
        result = api_manager.movies_api.get_movies(genre=genre)

        assert result['status_code'] == 200
        data = result['data']
        assert 'movies' in data
        assert len(data['movies']) == 10

    @pytest.mark.api
    def test_movies_invalid_genre_filter(self, api_manager, random_string):
        """Негатив: Случайный жанр - API возвращает обычный список"""
        result = api_manager.movies_api.get_movies(genre=random_string)

        assert result['status_code'] == 200
        data = result['data']
        assert len(data['movies']) == 10

    @pytest.mark.api
    def test_movies_invalid_pagination(self, api_manager):
        """Негатив: Неверные параметры - API возвращает 400"""
        result = api_manager.movies_api.get_movies(page=-1, limit=0)

        # API правильно возвращает 400 для невалидных параметров
        assert result['status_code'] == 400


    @pytest.mark.api
    def test_movies_response_structure(self, api_manager):
        """Проверка обязательной структуры ответа"""
        result = api_manager.movies_api.get_movies()

        assert result['status_code'] == 200
        data = result['data']
        assert all(key in data for key in ['movies', 'count'])

        for movie in data['movies']:
            required_fields = ['id', 'name', 'genreId', 'price', 'published', 'genre']
            assert all(field in movie for field in required_fields)
            assert 'name' in movie['genre']
