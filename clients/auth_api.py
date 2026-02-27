from constants.api_constants import AUTH_BASE_URL, REGISTER_ENDPOINT, LOGIN_ENDPOINT
from custom_requester.custom_requester import CustomRequester


class AuthApi(CustomRequester):
    def __init__(self, session):
        super().__init__(
            session=session,
            base_url=AUTH_BASE_URL
        )

    def register_user(self, user_data, expected_status=201):
        """
        Регистрация нового пользователя.
        :param user_data: Данные пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method='POST',
            endpoint=REGISTER_ENDPOINT,
            data=user_data,
            expected_status=expected_status
        )

    def login(self, login_data, expected_status=(200, 201)):
        return self.send_request(
            method='POST',
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status,
        )

    def login_and_get_token(self, login_data) -> str:
        response = self.login(login_data, expected_status=(200, 201))

        body = response.json()
        token = body.get('accessToken')

        if not token:
            raise KeyError(f'Токе не найден в ответе: {body}')

        return token
