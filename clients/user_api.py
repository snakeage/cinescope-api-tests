from constants import AUTH_BASE_URL
from custom_requester.custom_requester import CustomRequester


class UserApi(CustomRequester):
    def __init__(self, session):
        super().__init__(
            session=session,
            base_url=AUTH_BASE_URL
        )

    def get_user_info(self, user_id, expected_status=200):
        """
        Получение информации о пользователе.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method='GET',
            endpoint=f'/users/{user_id}',
            expected_status=expected_status
        )

    def delete_user(self, user_id, expected_status=200):
        """
        Удаление пользователя.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method='DELETE',
            endpoint=f'/user/{user_id}',
            expected_status=expected_status
        )