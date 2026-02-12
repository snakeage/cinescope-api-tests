from assertions.assert_user_contract import assert_user_contract
from assertions.auth_assertions import assert_login_success, assert_login_failed


class TestAuthApi:
    def test_register_user(self, api_manager, test_user):

        register_response = api_manager.auth_api.register_user(
            user_data=test_user,
        )

        data = register_response.json()
        assert_user_contract(
            data,
            data['email'],
            data['fullName']
        )


    def test_login_user(self, api_manager, registered_user):
        response = api_manager.auth_api.login({
            'email': registered_user['email'],
            'password': registered_user['_password'],
        })

        data = response.json()
        assert_login_success(data, registered_user['email'])

    def test_login_user_with_wrong_password_returns_401(self, api_manager, registered_user):
        bad_login_data = {
            'email': registered_user['email'],
            'password': 'WRONG_PASSWORD_123',
        }

        resp = api_manager.auth_api.login(bad_login_data, expected_status=401)

        data = resp.json()
        assert_login_failed(data)

    def test_login_user_with_nonexistent_email_returns_401(self, api_manager, registered_user):
        bad_login_data = {
            'email': 'WRONG_EMAIL@GMAIL.COM',
            'password': registered_user['_password'],
        }

        resp = api_manager.auth_api.login(bad_login_data, expected_status=401)

        data = resp.json()
        assert_login_failed(data)

    def test_login_user_with_empty_request_body_returns_401(self, api_manager):
        empty_login_data = {}

        resp = api_manager.auth_api.login(empty_login_data, expected_status=401)

        data = resp.json()
        assert_login_failed(data)
