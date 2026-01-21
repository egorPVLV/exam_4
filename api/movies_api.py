from constants import MOVIES_ENDPOINT


class MoviesAPI:
    def __init__(self, session, base_url=None):
        self.session = session
        self.base_url = base_url

    def get_movies(self, genre=None, page=1, limit=10):
        """Получить список фильмов с фильтрами и пагинацией"""
        params = {'page': page, 'limit': limit}
        if genre:
            params['genre'] = genre

        response = self.session.get(
            f"{self.base_url}{MOVIES_ENDPOINT}",
            params=params
        )

        return {
            'status_code': response.status_code,
            'data': response.json()
        }
