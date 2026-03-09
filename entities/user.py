from typing import Type, TypeVar, overload

import requests
from pydantic import BaseModel

from clients.api_manager import ApiManager

T = TypeVar('T', bound=BaseModel)


class User:
    def __init__(
        self,
        email: str,
        password: str,
        roles: list[str],
        api: ApiManager,
    ):
        self.email = email
        self.password = password
        self.roles = roles
        self.api = api
        self.id: str | None = None
        self.token: str | None = None
        self.full_name: str | None = None
        self.verified: bool | None = None

    @property
    def creds(self) -> dict[str, str]:
        return {'email': self.email, 'password': self.password}

    @overload
    def register(self, payload, expected_status: int = 201, *, response_model: Type[T]) -> T: ...

    @overload
    def register(
        self, payload, expected_status: int = 201, *, response_model: None = None
    ) -> requests.Response: ...

    def register(
        self, payload, expected_status: int = 201, *, response_model: Type[T] | None = None
    ):
        created = self.api.auth.register_user(
            payload, expected_status=expected_status, response_model=response_model
        )

        if response_model is not None:
            self.id = str(created.id)

        return created

    @overload
    def login(self, creds=None, expected_status: int = 200, *, response_model: Type[T]) -> T: ...

    @overload
    def login(
        self, creds=None, expected_status: int = 200, *, response_model: None = None
    ) -> requests.Response: ...

    def login(
        self, creds=None, expected_status: int = 200, *, response_model: Type[T] | None = None
    ):
        if creds is None:
            creds = self.creds

        return self.api.auth.login(
            creds, expected_status=expected_status, response_model=response_model
        )

    def authenticate(self):
        token = self.api.auth.login_and_get_token(self.creds)

        self.api.session.headers.update({'Authorization': f'Bearer {token}'})

        self.token = token

        return token

    @overload
    def get_user(self, locator, expected_status: int = 200, *, response_model: Type[T]) -> T: ...

    @overload
    def get_user(
        self, locator, expected_status: int = 200, *, response_model: None = None
    ) -> requests.Response: ...

    def get_user(
        self, locator, expected_status: int = 200, *, response_model: Type[T] | None = None
    ):
        return self.api.users.get_user(
            locator, expected_status=expected_status, response_model=response_model
        )

    @overload
    def create_user(self, payload, expected_status: int = 201, *, response_model: Type[T]) -> T: ...

    @overload
    def create_user(
        self, payload, expected_status: int = 201, *, response_model: None = None
    ) -> requests.Response: ...

    def create_user(
        self, payload, expected_status: int = 201, *, response_model: Type[T] | None = None
    ):
        return self.api.users.create_user(
            payload, expected_status=expected_status, response_model=response_model
        )

    def delete(self):
        return self.api.users.delete_user(self.id)
