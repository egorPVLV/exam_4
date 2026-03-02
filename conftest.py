

import pytest
import requests
from constants import BASE_URL, REGISTER_ENDPOINT, LOGIN_ENDPOINT, NAME, PASSWORD
from custom_requester.custom_requester import CustomRequester
from utils.data_generator import DataGenerator
from api.api_manager import ApiManager
import string
import random


@pytest.fixture(scope="session")
def test_user():

    name = NAME
    password = PASSWORD

    return {
        "fullName": name,
        "password": password,
        "passwordRepeat": password,
        "roles": ["SUPER_ADMIN"]
    }

@pytest.fixture(scope="session")
def registered_user(requester: CustomRequester, test_user: dict[str, str]):
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    response = requester.send_request(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=test_user,
        expected_status=201
    )
    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]
    return registered_user

@pytest.fixture(scope="session")
def requester():
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL)

@pytest.fixture(scope="session")
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def api_manager(session: requests.Session):
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session, base_url=BASE_URL)


@pytest.fixture(scope="session")
def random_string():
    """Генератор случайных строк"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=20))


@pytest.fixture(scope="session")
def create_movies(api_manager: ApiManager):
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

    return response.json()