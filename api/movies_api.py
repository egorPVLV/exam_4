from constants import MOVIES_ENDPOINT


class MoviesAPI:
    def __init__(self, session, base_url: str = None):
        self.session = session
        self.base_url = base_url

    def get_movies(self, genreId: int = 1, page: int = 1, pageSize: int = 10):
        """Получить список фильмов с фильтрами и пагинацией"""
        params = {'page': page, 'pageSize': pageSize, 'genreId': genreId}


        response = self.session.get(
            f"{self.base_url}{MOVIES_ENDPOINT}",
            params=params
        )

        return {
            'status_code': response.status_code,
            'data': response.json()
        }

    def post_movies(self, name: str = "Название фильма", imageUrl: str = "https://image.url", price: int = 100,
                    description: str = "Описание фильма", location: str = "SPB", published: bool = True,
                    genreId: int = 1):
        """Создание фильма"""
        data = {
            "name": name,
            "imageUrl": imageUrl,
            "price": price,
            "description": description,
            "location": location,
            "published": published,
            "genreId": genreId
        }

        response = self.session.post(
            f"{self.base_url}{MOVIES_ENDPOINT}",
            data=data
        )

        return {
            'status_code': response.status_code,
            'data': response.json()
        }


    def delete_movies(self, id: int = 1):
        """Удаление фильма"""
        params = {
            "id": id,
        }

        response = self.session.delete(
            f"{self.base_url}{MOVIES_ENDPOINT}",
            params=params
        )

        return {
            'status_code': response.status_code,
            'data': response.json()
        }

    def patch_movies(self, name: str = "Название фильма", imageUrl: str = "https://image.url", price: int = 100,
                    description: str = "Описание фильма", location: str = "SPB", published: bool = True,
                    genreId: int = 1,  id: int = 1):
        """Изменение фильма"""
        data = {
            "name": name,
            "imageUrl": imageUrl,
            "price": price,
            "description": description,
            "location": location,
            "published": published,
            "genreId": genreId
        }

        response = self.session.patch(
            f"{self.base_url}{MOVIES_ENDPOINT}",
            params=id,
            data=data
        )

        return {
            'status_code': response.status_code,
            'data': response.json()
        }
