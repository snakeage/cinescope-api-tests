from constants.api_constants import AUTH_BASE_URL
from custom_requester.custom_requester import CustomRequester


class UserApi(CustomRequester):
    def __init__(self, session):
        super().__init__(
            session=session,
            base_url=AUTH_BASE_URL
        )

    def get_user(self, locator, expected_status=200):
        return self.send_request(
            method='GET',
            endpoint=f'/user/{locator}',
            expected_status=expected_status
        )

    def create_user(self, user_data, expected_status=201):
        return self.send_request(
            method='POST',
            endpoint=f'/user',
            data=user_data,
            expected_status=expected_status
        )

    def delete_user(self, user_id, expected_status=200):
        return self.send_request(
            method='DELETE',
            endpoint=f'/user/{user_id}',
            expected_status=expected_status
        )
