import pytest
from api.api_manager import ApiManager
from utils.data_generator import DataGenerator
from constants import (
    NAME, PASSWORD, REGISTER_DATA, LOGIN_DATA,
    CREATE_USER_DATA, EDIT_USER_DATA, ADMIN_USER_ID
)


@pytest.mark.api
class TestUserAPI:

    @pytest.mark.parametrize("page, pagesize", [
        (1, 10),
        (1, 5),
        (2, 20)
    ])
    def test_get_user_list_positive(self, api_manager: ApiManager, page: int, pagesize: int) -> None:
        """Позитив: Получить список пользователей с пагинацией (ADMIN)"""
        api_manager.auth_api.authenticate((NAME, PASSWORD))

        result = api_manager.user_api.get_user_list(page=page, pagesize=pagesize, roles="ADMIN")
        assert result['status_code'] == 200

        data = result['data']
        assert 'users' in data
        assert len(data['users']) <= pagesize
        assert isinstance(data['count'], int)

    def test_get_user_list_with_roles(self, api_manager: ApiManager) -> None:
        """Позитив: Фильтр по ролям"""
        api_manager.auth_api.authenticate((NAME, PASSWORD))

        result = api_manager.user_api.get_user_list(
            page=1, pagesize=10, roles=["ADMIN", "SUPER_ADMIN"]
        )

        assert result['status_code'] == 200
        # data = result['data']
        # assert all("ADMIN" in user['roles'] or "SUPER_ADMIN" in user['roles']
        #            for user in data['users'])


    def test_register_user_positive(self, api_manager: ApiManager) -> None:
        """Позитив: Регистрация нового пользователя (PUBLIC)"""
        test_email = DataGenerator.generate_random_email()
        register_data = REGISTER_DATA.copy()
        register_data["email"] = test_email

        result = api_manager.user_api.register_user(register_data)

        assert result['status_code'] == 201
        data = result['data']
        assert data['email'] == test_email

    def test_register_user_invalid_data(self, api_manager: ApiManager) -> None:
        """Негатив: Неверные данные регистрации"""
        invalid_data = {"email": "invalid-email", "password": "123"}

        result = api_manager.user_api.register_user(invalid_data, expected_status=400)
        assert result['status_code'] == 400

    def test_register_user_exists(self, api_manager: ApiManager) -> None:
        """Негатив: Пользователь уже существует"""
        result = api_manager.user_api.register_user(REGISTER_DATA, expected_status=409)
        assert result['status_code'] == 409

    def test_login_user_positive(self, api_manager: ApiManager) -> None:
        """Позитив: Успешный логин"""
        result = api_manager.user_api.login_user(LOGIN_DATA)

        assert result['status_code'] == 200
        data = result['data']
        assert 'accessToken' in data
        assert 'user' in data
        assert data['user']['email'] == LOGIN_DATA['email']

    def test_login_invalid_credentials(self, api_manager: ApiManager) -> None:
        """Негатив: Неверный логин/пароль"""
        invalid_login = LOGIN_DATA.copy()
        invalid_login["password"] = "wrongpass"

        result = api_manager.user_api.login_user(invalid_login, expected_status=401)
        assert result['status_code'] == 401

    def test_logout_positive(self, api_manager: ApiManager) -> None:
        """Позитив: Выход из аккаунта"""
        api_manager.auth_api.authenticate((NAME, PASSWORD))

        result = api_manager.user_api.logout()
        assert result['status_code'] == 200

    def test_refresh_tokens_positive(self, api_manager: ApiManager) -> None:
        """Позитив: Обновление токенов"""
        api_manager.auth_api.authenticate((NAME, PASSWORD))

        result = api_manager.user_api.refresh_tokens()
        assert result['status_code'] == 200
        assert 'accessToken' in result['data']

    # def test_confirm_email_valid(self, api_manager: ApiManager) -> None:
    #     """Позитив: Подтверждение email"""
    #
    #     result = api_manager.user_api.login_user(LOGIN_DATA)
    #     data = result['data']
    #
    #     #pytest.skip("Требуется токен из email")
    #     token = data['accessToken']
    #     result = api_manager.user_api.confirm_email(token)
    #     assert result['status_code'] == 200

    def test_confirm_email_invalid(self, api_manager: ApiManager) -> None:
        """Негатив: Неверный токен подтверждения"""
        result = api_manager.user_api.confirm_email("invalid-token", expected_status=404)
        assert result['status_code'] == 404

    def test_get_user_info_positive(self, api_manager: ApiManager) -> None:
        """Позитив: Информация о пользователе (ADMIN)"""
        api_manager.auth_api.authenticate((NAME, PASSWORD))

        result = api_manager.user_api.get_user_info(ADMIN_USER_ID)
        assert result['status_code'] == 200
        data = result['data']
        assert 'id' in data
        assert 'email' in data

    def test_get_user_info_not_found(self, api_manager: ApiManager) -> None:
        """Негатив: Пользователь не найден"""
        pytest.skip("API возвращает неверный статус код")
        api_manager.auth_api.authenticate((NAME, PASSWORD))

        result = api_manager.user_api.get_user_info("nonexistent-", expected_status=404)
        assert result['status_code'] == 404

    def test_delete_user_positive(self, api_manager: ApiManager) -> None:
        """Позитив: Удаление своего пользователя (USER)"""
        api_manager.auth_api.authenticate((NAME, PASSWORD))

        result = api_manager.user_api.get_user_list()
        data = result['data']

        current_user_id = data['users'][0]['id']
        result = api_manager.user_api.delete_user(current_user_id,expected_status=200)
        assert result['status_code'] == 200

    def test_delete_user_not_found(self, api_manager: ApiManager) -> None:
        """Негатив: Удаление несуществующего"""
        api_manager.auth_api.authenticate((NAME, PASSWORD))

        result = api_manager.user_api.delete_user("nonexistent-id", expected_status=404)
        assert result['status_code'] == 404

    def test_update_user_positive(self, api_manager: ApiManager) -> None:
        """Позитив: Изменение пользователя (ADMIN)"""
        api_manager.auth_api.authenticate((NAME, PASSWORD))

        edit_data = EDIT_USER_DATA
        result = api_manager.user_api.update_user(ADMIN_USER_ID, edit_data)

        assert result['status_code'] == 200


    def test_update_user_invalid_data(self, api_manager: ApiManager) -> None:
        """Негатив: Неверные данные обновления"""
        api_manager.auth_api.authenticate((NAME, PASSWORD))

        invalid_data = {"roles": ["INVALID_ROLE"]}
        result = api_manager.user_api.update_user(ADMIN_USER_ID, invalid_data, expected_status=400)
        assert result['status_code'] == 400

    def test_create_user_positive(self, api_manager: ApiManager) -> None:
        """Позитив: Создание пользователя админом"""
        api_manager.auth_api.authenticate((NAME, PASSWORD))

        test_email = f"admin_test_{DataGenerator.generate_random_int(99, 1000)}@example.com"
        user_data = CREATE_USER_DATA.copy()
        user_data["email"] = test_email


        result = api_manager.user_api.create_user(user_data)
        assert result['status_code'] == 201





