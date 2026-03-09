from typing import Type, TypeVar, overload

import requests
from pydantic import BaseModel

from constants.api_constants import API_BASE_URL, MOVIES
from custom_requester.custom_requester import CustomRequester

T = TypeVar('T', bound=BaseModel)


class MoviesApi(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=API_BASE_URL)

    @overload
    def get_movies(
        self,
        expected_status: int = 200,
        *,
        response_model: Type[T],
        **params,
    ) -> T: ...

    @overload
    def get_movies(
        self,
        expected_status: int = 200,
        *,
        response_model: None = None,
        **params,
    ) -> requests.Response: ...

    def get_movies(
        self,
        expected_status: int = 200,
        *,
        response_model: Type[T] | None = None,
        **params,
    ):
        return self.get(
            endpoint=MOVIES,
            params=params,
            expected_status=expected_status,
            response_model=response_model,
        )

    @overload
    def create_movie(
        self,
        data,
        expected_status: int = 201,
        *,
        response_model: Type[T],
    ) -> T: ...

    @overload
    def create_movie(
        self,
        data,
        expected_status: int = 201,
        *,
        response_model: None = None,
    ) -> requests.Response: ...

    def create_movie(
        self,
        data,
        expected_status: int = 201,
        *,
        response_model: Type[T] | None = None,
    ):
        return self.post(
            endpoint=MOVIES,
            data=data,
            expected_status=expected_status,
            response_model=response_model,
        )

    @overload
    def get_movie(
        self,
        movie_id,
        expected_status: int = 200,
        *,
        response_model: Type[T],
    ) -> T: ...

    @overload
    def get_movie(
        self,
        movie_id,
        expected_status: int = 200,
        *,
        response_model: None = None,
    ) -> requests.Response: ...

    def get_movie(
        self,
        movie_id,
        expected_status: int = 200,
        *,
        response_model: Type[T] | None = None,
    ):
        return self.get(
            endpoint=f'{MOVIES}/{movie_id}',
            expected_status=expected_status,
            response_model=response_model,
        )

    @overload
    def update_movie(
        self,
        movie_id,
        data,
        expected_status: int = 200,
        *,
        response_model: Type[T],
    ) -> T: ...

    @overload
    def update_movie(
        self,
        movie_id,
        data,
        expected_status: int = 200,
        *,
        response_model: None = None,
    ) -> requests.Response: ...

    def update_movie(
        self,
        movie_id,
        data,
        expected_status: int = 200,
        *,
        response_model: Type[T] | None = None,
    ):
        return self.patch(
            endpoint=f'{MOVIES}/{movie_id}',
            data=data,
            expected_status=expected_status,
            response_model=response_model,
        )

    @overload
    def delete_movie(
        self,
        movie_id,
        expected_status: int = 200,
        *,
        response_model: Type[T],
    ) -> T: ...

    @overload
    def delete_movie(
        self,
        movie_id,
        expected_status: int = 200,
        *,
        response_model: None = None,
    ) -> requests.Response: ...

    def delete_movie(
        self,
        movie_id,
        expected_status: int = 200,
        *,
        response_model: Type[T] | None = None,
    ):
        return self.delete(
            endpoint=f'{MOVIES}/{movie_id}',
            expected_status=expected_status,
            response_model=response_model,
        )
