from typing import List, Optional, Type, TypeVar, overload

import requests
from pydantic import BaseModel

from clients.api_manager import ApiManager

T = TypeVar('T', bound=BaseModel)


class Movie:
    def __init__(self, api: ApiManager, data=None):
        self.api = api
        self.id = None
        self.data = data

        if data and 'id' in data:
            self.id = data['id']

    @property
    def name(self):
        return self.data.get('name') if isinstance(self.data, dict) else None

    @overload
    def create(
        self,
        payload,
        expected_status: int = 201,
        *,
        response_model: Type[T],
    ) -> T: ...

    @overload
    def create(
        self,
        payload,
        expected_status: int = 201,
        *,
        response_model: None = None,
    ) -> requests.Response: ...

    def create(self, payload, expected_status: int = 201, *, response_model: Type[T] | None = None):
        result = self.api.movies.create_movie(
            payload, expected_status=expected_status, response_model=response_model
        )

        if response_model is not None:
            self.id = result.id
            self.data = result.model_dump(by_alias=True)

        return result

    @overload
    def get(
        self,
        movie_id=None,
        expected_status: int = 200,
        *,
        response_model: Type[T],
    ) -> T: ...

    @overload
    def get(
        self, movie_id=None, expected_status: int = 200, *, response_model: None = None
    ) -> requests.Response: ...

    def get(
        self,
        movie_id=None,
        expected_status: int = 200,
        *,
        response_model: Type[T] | None = None,
    ):
        target_id = movie_id or self.id

        result = self.api.movies.get_movie(
            target_id, expected_status=expected_status, response_model=response_model
        )

        if response_model is not None:
            self.id = result.id
            self.data = result.model_dump(by_alias=True)

        return result

    @overload
    def update(
        self,
        payload=None,
        movie_id=None,
        expected_status: int = 200,
        *,
        response_model: Type[T],
    ) -> T: ...

    @overload
    def update(
        self,
        payload=None,
        movie_id=None,
        expected_status: int = 200,
        *,
        response_model: None = None,
    ) -> requests.Response: ...

    def update(
        self,
        payload=None,
        movie_id=None,
        expected_status: int = 200,
        *,
        response_model: Type[T] | None = None,
    ):
        target_id = movie_id or self.id

        if not target_id:
            raise ValueError('Movie id не задан.')

        result = self.api.movies.update_movie(
            target_id, payload, expected_status=expected_status, response_model=response_model
        )

        if response_model is not None:
            self.id = result.id
            self.data = result.model_dump(by_alias=True)

        return result

    @overload
    def delete(
        self,
        movie_id=None,
        expected_status: int = 200,
        *,
        response_model: Type[T],
    ) -> T: ...

    @overload
    def delete(
        self,
        movie_id=None,
        expected_status: int = 200,
        *,
        response_model: None = None,
    ) -> requests.Response: ...

    def delete(
        self,
        movie_id=None,
        expected_status: int = 200,
        *,
        response_model: Type[T] | None = None,
    ):
        target_id = movie_id or self.id

        if not target_id:
            raise ValueError('Movie id не задан.')

        resp = self.api.movies.delete_movie(
            target_id, expected_status=expected_status, response_model=response_model
        )

        return resp

    @overload
    def get_movies(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
        locations: Optional[List[str]] = None,
        published: Optional[bool] = None,
        genre_id: Optional[int] = None,
        created_at: Optional[str] = None,
        expected_status: int = 200,
        *,
        response_model: Type[T],
    ) -> T: ...

    @overload
    def get_movies(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
        locations: Optional[List[str]] = None,
        published: Optional[bool] = None,
        genre_id: Optional[int] = None,
        created_at: Optional[str] = None,
        expected_status: int = 200,
        *,
        response_model: None = None,
    ) -> requests.Response: ...

    def get_movies(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
        locations: Optional[List[str]] = None,
        published: Optional[bool] = None,
        genre_id: Optional[int] = None,
        created_at: Optional[str] = None,
        expected_status: int = 200,
        *,
        response_model: Type[T] | None = None,
    ):
        params = {
            'page': page,
            'pageSize': page_size,
            'minPrice': min_price,
            'maxPrice': max_price,
            'locations': locations,
            'published': published,
            'genreId': genre_id,
            'createdAt': created_at,
        }

        params = {k: v for k, v in params.items() if v is not None}

        return self.api.movies.get_movies(
            expected_status=expected_status, response_model=response_model, **params
        )
