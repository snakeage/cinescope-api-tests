from constants.api_constants import MOVIES, API_BASE_URL
from custom_requester.custom_requester import CustomRequester


class MoviesApi(CustomRequester):
    def __init__(self, session):
        super().__init__(
            session=session,
            base_url=API_BASE_URL
        )

    def get_movies(self, expected_status=200, **params):
        return self.get(
            endpoint=MOVIES,
            params=params,
            expected_status=expected_status
        )

    def create_movie(self, data, expected_status=201):
        return self.post(
            endpoint=MOVIES,
            data=data,
            expected_status=expected_status
        )

    def get_movie(self, movie_id, expected_status=200):
        return self.get(
            endpoint=f'{MOVIES}/{movie_id}',
            expected_status=expected_status
        )

    def update_movie(self, movie_id, data, expected_status=200):
        return self.patch(
            endpoint=f'{MOVIES}/{movie_id}',
            data=data,
            expected_status=expected_status
        )

    def delete_movie(self, movie_id, expected_status=200):
        return self.delete(
            endpoint=f'{MOVIES}/{movie_id}',
            expected_status=expected_status
        )
