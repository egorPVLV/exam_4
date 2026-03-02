from requests import Session, Response

from constants import MOVIES_ENDPOINT, BASE_URL, GENRES_ENDPOINT
from custom_requester.custom_requester import CustomRequester


class MoviesAPI(CustomRequester):
    def __init__(self, session: Session):
        super().__init__(session=session, base_url=BASE_URL)

    def create_movie(self, movie_data: dict, expected_status: int = 201) -> Response:
        """
        movie_data = {
            "name": name,
            "imageUrl": imageUrl,
            "price": price,
            "description": description,
            "location": location,
            "published": published,
            "genreId": genreId
        }
        """
        return self.send_request(
            method="POST",
            endpoint=MOVIES_ENDPOINT,
            data=movie_data,
            expected_status=expected_status
        )

    def genre_id(self):
        response = self.send_request(
            method="GET",
            endpoint=GENRES_ENDPOINT,
            data=None,
            expected_status=200
        )

        result = list(map(lambda x: x['id'], response.json()))[0]
        return result


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


    def delete_movies(self, id: int):
        """Удаление фильма"""

        response = self.session.delete(
            f"{self.base_url}{MOVIES_ENDPOINT}/{id}"
        )

        return {
            'status_code': response.status_code,
            'data': response.json()
        }

    def patch_movies(self, movie_data: dict,  id: int, expected_status: int = 200):
        """Изменение фильма"""


        response = self.send_request(
            method="PATCH",
            endpoint=MOVIES_ENDPOINT+"/"+str(id),
            data=movie_data,
            expected_status=200
        )
        return {
            'status_code': response.status_code,
            'data': response.json()
        }
