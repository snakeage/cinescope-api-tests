from typing import Optional, List

from clients.api_manager import ApiManager


class Movie:
    def __init__(
            self,
            api: ApiManager,
            data=None
    ):
        self.api = api
        self.id = None
        self.data = data

        if data and 'id' in data:
            self.id = data['id']

    @property
    def name(self):
        return self.data.get('name') if self.data else None

    def create(self, payload, expected_status=201):
        resp = self.api.movies.create_movie(
            payload,
            expected_status=expected_status
        )

        body = resp.json()

        self.data = body
        self.id = body.get('id')

        return resp

    def get(self, movie_id=None, expected_status=200):
        target_id = movie_id or self.id

        resp = self.api.movies.get_movie(
            target_id,
            expected_status=expected_status
        )

        if resp.status_code == 200:
            self.data = resp.json()
            self.id = self.data['id']

        return resp

    def update(self, payload=None, movie_id=None, expected_status=200):
        target_id = movie_id or self.id

        if not target_id:
            raise ValueError('Movie id не задан.')

        resp = self.api.movies.update_movie(
            target_id,
            payload,
            expected_status=expected_status
        )

        if resp.status_code == 200:
            self.data = resp.json()
            self.id = self.data['id']

        return resp

    def delete(self, movie_id=None, expected_status=200):
        target_id = movie_id or self.id

        if not target_id:
            raise ValueError('Movie id не задан.')

        resp = self.api.movies.delete_movie(
            target_id,
            expected_status=expected_status
        )

        return resp

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
    ):
        params = {
            "page": page,
            "pageSize": page_size,
            "minPrice": min_price,
            "maxPrice": max_price,
            "locations": locations,
            "published": published,
            "genreId": genre_id,
            "createdAt": created_at,
        }

        params = {k: v for k, v in params.items() if v is not None}

        return self.api.movies.get_movies(
            expected_status=expected_status,
            **params
        )
