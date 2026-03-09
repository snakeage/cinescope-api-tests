import pytest

from assertions.auth_assertions import assert_get_user_forbidden, assert_login_failed
from constants.roles import Roles
from models.admin_models import AdminCreateUserResponse
from models.get_user_models import GetUserResponse
from models.login_models import LoginResponse
from models.register_models import RegisterUserResponse
from utils.data_generator import DataGenerator
from utils.user_payloads import generate_admin_user_payload, generate_register_payload

pytestmark = pytest.mark.api


class TestAuthApi:
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_register_user(self, auth_api):
        payload, _ = generate_register_payload()

        user = auth_api.register_user(payload, response_model=RegisterUserResponse)

        assert user.email == payload.email
        assert user.full_name == payload.full_name
        assert Roles.USER in user.roles
        assert user.verified is True

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_login_user(self, auth_api):
        payload, password = generate_register_payload()

        auth_api.register_user(payload)

        login_data = {'email': payload.email, 'password': password}

        login = auth_api.login(login_data, response_model=LoginResponse)

        assert login.user.email == payload.email
        assert Roles.USER in login.user.roles
        assert login.access_token

    @pytest.mark.negative
    @pytest.mark.regression
    def test_login_user_with_wrong_password_returns_401(self, auth_api):
        payload, password = generate_register_payload()

        auth_api.register_user(payload)

        resp = auth_api.login(
            {'email': payload.email, 'password': f'{password}_WRONG_PASSWORD'}, expected_status=401
        )

        assert_login_failed(resp)

    @pytest.mark.negative
    @pytest.mark.regression
    def test_login_user_with_nonexistent_email_returns_401(self, auth_api):
        payload, password = generate_register_payload()

        auth_api.register_user(payload)

        bad_login_data = {
            'email': DataGenerator.generate_wrong_random_email(),
            'password': password,
        }

        resp = auth_api.login(bad_login_data, expected_status=401)

        assert_login_failed(resp)

    @pytest.mark.negative
    @pytest.mark.regression
    def test_login_user_with_empty_request_body_returns_401(self, auth_api):
        payload, password = generate_register_payload()

        auth_api.register_user(payload)

        empty_login_data = {}

        resp = auth_api.login(empty_login_data, expected_status=401)

        assert_login_failed(resp)

    @pytest.mark.negative
    @pytest.mark.regression
    @pytest.mark.slow
    def test_get_user_by_id_forbidden_for_common_user(self, common_user):
        resp = common_user.get_user(common_user.id, expected_status=403)

        assert_get_user_forbidden(resp)

    @pytest.mark.negative
    @pytest.mark.regression
    @pytest.mark.slow
    def test_get_user_by_email_forbidden_for_common_user(self, common_user):
        resp = common_user.get_user(common_user.email, expected_status=403)

        assert_get_user_forbidden(resp)

    @pytest.mark.regression
    @pytest.mark.slow
    def test_super_admin_can_get_user(self, super_admin, common_user):
        user = super_admin.get_user(common_user.id, response_model=GetUserResponse)

        assert user.email == common_user.email
        assert [r.value for r in user.roles] == common_user.roles

    @pytest.mark.regression
    def test_create_user(self, super_admin):
        payload, _ = generate_admin_user_payload()

        user = super_admin.create_user(payload, response_model=AdminCreateUserResponse)

        assert user.email == payload.email
        assert user.full_name == payload.full_name
        assert user.verified is True
        assert Roles.USER in user.roles
