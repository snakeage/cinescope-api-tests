from datetime import datetime

from assertions.assert_user_contract import assert_user_contract, assert_login_contract, assert_user_created, \
    assert_user_response
from assertions.auth_assertions import assert_login_failed, assert_get_user_forbidden
from conftest import common_user
from constants.roles import Roles
from utils.user_payloads import generate_register_payload, generate_admin_user_payload


class TestAuthApi:
    def test_register_user(self, auth_api):
        payload, _ = generate_register_payload()

        resp = auth_api.register_user(payload)

        assert_user_contract(
            resp,
            payload['email'],
            payload['fullName']
        )

    def test_login_user(self, auth_api):
        payload, password = generate_register_payload()

        auth_api.register_user(payload)

        resp = auth_api.login({
            'email': payload['email'],
            'password': password
        })

        assert_login_contract(resp, payload['email'])

    def test_login_user_with_wrong_password_returns_401(self, auth_api):
        payload, password = generate_register_payload()

        auth_api.register_user(payload)

        resp = auth_api.login({
            'email': payload['email'],
            'password': f'{password}_WRONG_PASSWORD'
        },
            expected_status=401)

        assert_login_failed(resp)

    def test_login_user_with_nonexistent_email_returns_401(self, auth_api):
        payload, password = generate_register_payload()

        auth_api.register_user(payload)

        bad_login_data = {
            'email': f'WRONG_EMAIL_{payload["email"]}',
            'password': password,
        }

        resp = auth_api.login(bad_login_data, expected_status=401)

        assert_login_failed(resp)

    def test_login_user_with_empty_request_body_returns_401(self, auth_api):
        payload, password = generate_register_payload()

        auth_api.register_user(payload)

        empty_login_data = {}

        resp = auth_api.login(empty_login_data, expected_status=401)

        assert_login_failed(resp)

    def test_get_user_by_id_forbidden_for_common_user(self, common_user):
        resp = common_user.get_user(common_user.id, expected_status=403)

        assert_get_user_forbidden(resp)

    def test_get_user_by_email_forbidden_for_common_user(self, common_user):
        resp = common_user.get_user(common_user.email, expected_status=403)

        assert_get_user_forbidden(resp)

    def test_super_admin_can_get_user(self, super_admin, common_user):
        resp = super_admin.get_user(common_user.id)
        data = assert_user_contract(resp, common_user.email, common_user.full_name)

        assert data['roles'] == common_user.roles

    def test_create_user(self, super_admin):
        payload, password = generate_admin_user_payload()

        resp = super_admin.create_user(payload)

        assert_user_contract(resp, payload['email'], payload['fullName'])
