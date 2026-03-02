from typing import TypeVar, Type, overload

import requests
from pydantic import BaseModel

from constants.api_constants import AUTH_BASE_URL
from custom_requester.custom_requester import CustomRequester

T = TypeVar('T', bound=BaseModel)


class UserApi(CustomRequester):
    def __init__(self, session):
        super().__init__(
            session=session,
            base_url=AUTH_BASE_URL
        )

    @overload
    def get_user(
            self,
            locator,
            expected_status: int = 200,
            *,
            response_model: Type[T]
    ) -> T:
        ...

    @overload
    def get_user(
            self,
            locator,
            expected_status: int = 200,
            *,
            response_model: None = None
    ) -> requests.Response:
        ...

    def get_user(
            self,
            locator,
            expected_status: int = 200,
            *,
            response_model: Type[T] | None = None
    ):
        return self.send_request(
            method='GET',
            endpoint=f'/user/{locator}',
            expected_status=expected_status,
            response_model=response_model
        )

    @overload
    def create_user(
            self,
            user_data,
            expected_status: int = 201,
            *,
            response_model: Type[T]
    ) -> T:
        ...

    @overload
    def create_user(
            self,
            user_data,
            expected_status: int = 201,
            *,
            response_model: None = None
    ) -> requests.Response:
        ...

    def create_user(
            self,
            user_data,
            expected_status: int = 201,
            *,
            response_model: Type[T] | None = None
    ):
        return self.send_request(
            method='POST',
            endpoint=f'/user',
            data=user_data,
            expected_status=expected_status,
            response_model=response_model
        )

    def delete_user(self, user_id, expected_status=200):
        return self.send_request(
            method='DELETE',
            endpoint=f'/user/{user_id}',
            expected_status=expected_status
        )
