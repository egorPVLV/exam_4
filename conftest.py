

import pytest
import requests
from constants import BASE_URL, REGISTER_ENDPOINT, LOGIN_ENDPOINT, NAME, PASSWORD
from custom_requester.custom_requester import CustomRequester
from utils.data_generator import DataGenerator
from api.api_manager import ApiManager



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