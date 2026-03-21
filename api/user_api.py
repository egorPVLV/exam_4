from custom_requester.custom_requester import CustomRequester


class UserAPI(CustomRequester):
    """
    Класс для работы с API пользователей.
    """

    def __init__(self, session, base_url: str = None):
        super().__init__(session, base_url=base_url)
        self.session = session

    def register_user(self, user_data: dict, expected_status: int = 201):
        """POST /user - Создание пользователя"""
        response = self.send_request(
            method="POST",
            endpoint="/register",
            data=user_data,
            expected_status=expected_status
        )

        return {
            'status_code': response.status_code,
            'data': response.json()
        }



    def login_user(self, login_data: dict, expected_status: int = 200):
        """POST /login - Аутентификация (PUBLIC)"""
        response = self.send_request(
            method="POST",
            endpoint="/login",
            data=login_data,
            expected_status=expected_status
        )

        return {
            'status_code': response.status_code,
            'data': response.json()
        }

    def logout(self, expected_status: int = 200):
        """GET /logout - Выход из аккаунта"""
        response =  self.send_request(
            method="GET",
            endpoint="/logout",
            expected_status=expected_status
        )

        return {
            'status_code': response.status_code
        }

    def refresh_tokens(self, expected_status: int = 200):
        """GET /refresh-tokens - Обновление токенов"""
        response =  self.send_request(
            method="GET",
            endpoint="/refresh-tokens",
            expected_status=expected_status
        )

        return {
            'status_code': response.status_code,
            'data': response.json()
        }




    def confirm_email(self, token: str, expected_status: int = 200):
        """GET /confirm/{token} - Подтверждение email"""
        response =  self.send_request(
            method="GET",
            endpoint=f"/confirm/{token}",
            expected_status=expected_status
        )

        return {
            'status_code': response.status_code,
            'data': response.json()
        }

    def get_user_info(self, user_id: int | str, expected_status: int = 200):
        """
        Получение информации о пользователе.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        response =  self.send_request(
            method="GET",
            endpoint=f"/user/{user_id}",
            expected_status=expected_status
        )

        return {
            'status_code': response.status_code,
            'data': response.json()
        }

    def delete_user(self, user_id: int | str, expected_status: int = 204):
        """
        Удаление пользователя.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        response =  self.send_request(
            method="DELETE",
            endpoint=f"/user/{user_id}",
            expected_status=expected_status
        )

        return {
            'status_code': response.status_code
        }

    def update_user(self, user_id: int, user_data: dict, expected_status: int = 200):
        """PATCH /user/{id} - Изменение данных пользователя"""
        response =  self.send_request(
            method="PATCH",
            endpoint=f"/user/{user_id}",
            data=user_data,
            expected_status=expected_status
        )

        return {
            'status_code': response.status_code,
            'data': response.json()
        }

    def create_user(self, user_data: dict, expected_status: int = 201):
        """POST /user - Создание пользователя (ADMIN)"""
        response =  self.send_request(
            method="POST",
            endpoint="/user",  # ← /user, НЕ /register!
            data=user_data,
            expected_status=expected_status
        )

        return {
            'status_code': response.status_code,
            'data': response.json()
        }

    def get_user_list(self, page: int = 1, pagesize: int = 10, roles: str = None,
                      createdat: str = "asc", expected_status: int = 200):
        """GET /user - Список пользователей"""
        params_str = f"?page={page}&pageSize={pagesize}&createdAt={createdat}"
        if roles:
            params_str = f"?page={page}&pageSize={pagesize}&createdAt={createdat}&roles={roles}"

        response = self.send_request(
            method="GET",
            endpoint="/user" + params_str,
            expected_status=expected_status
        )

        return {
            'status_code': response.status_code,
            'data': response.json()
        }

