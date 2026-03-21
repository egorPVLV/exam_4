from requests import Session, Response
from unicodedata import name

from constants import MOVIES_ENDPOINT, BASE_URL, GENRES_ENDPOINT,REVIEW_ENDPOINT
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

    def create_reviews(self, id: int, rating: int=5, text: str="Хорошо"):
        """Создание отзыва к фильму"""
        review_data = {
            "rating": rating,
            "text": text
        }

        response = self.send_request(
            method="POST",
            endpoint=f"{MOVIES_ENDPOINT}/{str(id)}{REVIEW_ENDPOINT}",
            data=review_data,
            expected_status=201
        )

        return {
            'status_code': response.status_code,
            'data': response.json()
        }

    def get_reviews(self, id: int):

        response = self.send_request(
            method="GET",
            endpoint=f"{MOVIES_ENDPOINT}/{str(id)}{REVIEW_ENDPOINT}",
            expected_status=200
        )

        return {
            'status_code': response.status_code,
            'data': response.json()
        }

    def put_reviews(self, id: int, rating: int = 5, text: str = "Хорошо"):
        """Создание отзыва к фильму"""
        review_data = {
            "rating": rating,
            "text": text
        }

        response = self.send_request(
            method="PUT",
            endpoint=f"{MOVIES_ENDPOINT}/{str(id)}{REVIEW_ENDPOINT}",
            data=review_data,
            expected_status=200
        )

        return {
            'status_code': response.status_code,
            'data': response.json()
        }

    def delete_reviews(self, id: int):

        response = self.send_request(
            method="DELETE",
            endpoint=f"{MOVIES_ENDPOINT}/{str(id)}{REVIEW_ENDPOINT}",
            expected_status=200
        )

        return {
            'status_code': response.status_code,
            'data': response.json()
        }

    def genre_id(self):
        response = self.send_request(
            method="GET",
            endpoint=GENRES_ENDPOINT,
            expected_status=200,
            need_logging= False
        )

        result = list(map(lambda x: x['id'], response.json()))[0]
        return result

    def create_genre(self, name:str):
        response = self.send_request(
            method="POST",
            endpoint=GENRES_ENDPOINT,
            expected_status=201,
            need_logging= True,
            data={"name":name}
        )

        return {
            'status_code': response.status_code,
            'data': response.json()
        }

    def get_genre(self, id:int):
        response = self.send_request(
            method="GET",
            endpoint=f"{GENRES_ENDPOINT}/{id}",
            expected_status=200,
            need_logging=True
        )

        return {
            'status_code': response.status_code,
            'data': response.json()
        }

    def delete_genre(self, id:int):
        response = self.send_request(
            method="DELETE",
            endpoint=f"{GENRES_ENDPOINT}/{id}",
            expected_status=200,
            need_logging=True
        )

        return {
            'status_code': response.status_code,
            'data': response.json()
        }