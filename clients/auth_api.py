from typing import Type, TypeVar, overload

import requests
from pydantic import BaseModel

from constants.api_constants import AUTH_BASE_URL, LOGIN_ENDPOINT, REGISTER_ENDPOINT
from custom_requester.custom_requester import CustomRequester
from models.login_models import LoginResponse

T = TypeVar('T', bound=BaseModel)


class AuthApi(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=AUTH_BASE_URL)

    @overload
    def register_user(
        self, user_data, expected_status: int = 201, *, response_model: Type[T]
    ) -> T: ...

    @overload
    def register_user(
        self, user_data, expected_status: int = 201, *, response_model: None = None
    ) -> requests.Response: ...

    def register_user(
        self, user_data, expected_status: int = 201, *, response_model: Type[T] | None = None
    ):
        return self.send_request(
            method='POST',
            endpoint=REGISTER_ENDPOINT,
            data=user_data,
            expected_status=expected_status,
            response_model=response_model,
        )

    @overload
    def login(self, login_data, expected_status: int = 200, *, response_model: Type[T]) -> T: ...

    @overload
    def login(
        self, login_data, expected_status: int = 200, *, response_model: None = None
    ) -> requests.Response: ...

    def login(
        self, login_data, expected_status: int = 200, *, response_model: Type[T] | None = None
    ):
        return self.send_request(
            method='POST',
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status,
            response_model=response_model,
        )

    @overload
    def login_for_setup(self, login_data, *, response_model: Type[T]) -> T: ...

    @overload
    def login_for_setup(self, login_data, *, response_model: None = None) -> requests.Response: ...

    # TODO: remove after backend fixes /login status to stable 200 (now it may return 201).
    def login_for_setup(self, login_data, *, response_model: Type[T] | None = None):
        return self.send_request(
            method='POST',
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=(200, 201),
            response_model=response_model,
        )

    def login_and_get_token(self, login_data) -> str:
        # TODO: switch back to self.login(...) after backend fixes /login status to 200.
        login_response = self.login_for_setup(login_data, response_model=LoginResponse)

        return login_response.access_token
