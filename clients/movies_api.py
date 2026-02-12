from constants import MOVIES, API_BASE_URL
from custom_requester.custom_requester import CustomRequester

class MoviesApi(CustomRequester):
    def __init__(self, session):
        super().__init__(
            session = session,
            base_url=API_BASE_URL
        )

    def get_movies(self, params=None, expected_status=200):
        return self.send_request(
            method='GET',
            endpoint=MOVIES,
            params=params,
            expected_status=expected_status
        )

    def create_movie(self, payload, expected_status=201):
        return self.send_request(
            method='POST',
            endpoint=MOVIES,
            data=payload,
            expected_status=expected_status
        )

    def get_movie(self, movie_id, expected_status=200):
        return self.send_request(
            method='GET',
            endpoint=f'{MOVIES}/{movie_id}',
            expected_status=expected_status
        )

    def update_movie(self, movie_id, payload, expected_status=201):
        return self.send_request(
            method='PATCH',
            endpoint=f'{MOVIES}/{movie_id}',
            data=payload,
            expected_status=expected_status
        )

    def delete_movie(self, movie_id, expected_status=200):
        return self.send_request(
            method='DELETE',
            endpoint=f'{MOVIES}/{movie_id}',
            expected_status=expected_status
        )