from datetime import datetime

import pytest

from assertions.movies_assertions import assert_movies_contract, assert_movie_contract, assert_bad_request, \
    assert_conflict, assert_not_found, assert_unauthorized, assert_forbidden
from conftest import common_user
from constants.roles import Roles
from entities.movie import Movie
from utils.movie_payloads import MovieDataGenerator


class TestMoviesApi:
    def test_get_movies(self, unauthorized_movies):
        resp = unauthorized_movies.get_movies()

        assert_movies_contract(resp)

    def test_get_movies_filter_by_location(self, unauthorized_movies):
        resp = unauthorized_movies.get_movies(
            locations=['MSK']
        )

        data = assert_movies_contract(resp)

        movies = data['movies']
        assert movies, 'Фильтр по location вернул пустой список'

        for movie in movies:
            assert movie['location'] == 'MSK'

    def test_get_movies_filter_by_price_range(self, unauthorized_movies):
        resp = unauthorized_movies.get_movies(
            min_price=100,
            max_price=1000
        )

        data = assert_movies_contract(resp)

        movies = data['movies']
        for movie in movies:
            assert 100 <= movie['price'] <= 1000


    def test_get_movies_filter_by_published(self, unauthorized_movies):
        resp = unauthorized_movies.get_movies(
            published=True
        )

        data = assert_movies_contract(resp)

        movies = data['movies']
        for movie in movies:
            assert movie['published'] is True



    def test_get_movies_sorted_by_created_at_desc(self, unauthorized_movies):
        resp = unauthorized_movies.get_movies(
            created_at='desc'
        )

        data = assert_movies_contract(resp)

        movies = data['movies']
        dates = [
            datetime.fromisoformat(movie['createdAt'].replace("Z", "+00:00"))
            for movie in movies
        ]

        assert dates == sorted(dates, reverse=True)



    def test_get_movies_pagination(self, unauthorized_movies):
        resp = unauthorized_movies.get_movies(
            page=1,
            page_size=10
        )

        data = assert_movies_contract(resp)

        movies = data['movies']
        assert len(movies) <= 10
        assert data['page'] == 1
        assert data['pageSize'] == 10



    def test_get_movies_with_invalid_param_returns_400(self, unauthorized_movies):
        resp = unauthorized_movies.get_movies(
            page='Invalid',
            expected_status=400
        )

        assert_bad_request(resp)

    def test_create_movie(self, movie, movie_data):
        resp = movie.create(movie_data)

        assert_movie_contract(resp)

    def test_create_movie_with_invalid_name_returns_400(self, movie):
        payload = MovieDataGenerator.movie_payload(name=123)
        resp = movie.create(payload, expected_status=400)

        assert_bad_request(resp)

    def test_create_movie_with_existing_name_returns_409(self, movie, created_movie):

        payload = MovieDataGenerator.movie_payload(
            name=created_movie.name
        )

        resp = movie.create(
            payload, expected_status=409
        )

        assert_conflict(resp)

    def test_get_movie(self, created_movie):
        resp = created_movie.get()

        assert_movie_contract(resp)

    def test_get_movie_with_nonexisting_id_returns_404(self, movie):
        resp = movie.get(movie_id=9999999, expected_status=404)

        assert_not_found(resp)

    def test_delete_movie(self, created_movie):
        resp = created_movie.delete()

        assert_movie_contract(resp)

        created_movie.get(expected_status=404)

    def test_delete_movie_with_nonexisting_id_returns_404(self, created_movie):
        resp = created_movie.delete(movie_id=99999999, expected_status=404)

        assert_not_found(resp)

    def test_delete_movie_with_unauthorized_user_returns_401(
            self,
            unauthorized_movie
    ):

        resp = unauthorized_movie.delete(expected_status=401)

        assert_unauthorized(resp)

    def test_delete_movie_with_non_admin_user_returns_403(
            self,
            registered_movie
    ):

        resp = registered_movie.delete(expected_status=403)

        assert_forbidden(resp)

    def test_update_movies_name(self, created_movie):
        old_name = created_movie.name

        patched_payload = {'name': old_name + '_patched'}

        resp = created_movie.update(
            patched_payload,
            expected_status=200
        )

        data = assert_movie_contract(resp)

        assert data['name'] != old_name, 'Название фильма не обновилось'
        assert data['name'] == patched_payload['name']

    def test_update_movie_with_nonexisting_id_returns_404(
            self,
            movie
    ):

        patched_payload = {'name': 'name_patched'}

        resp = movie.update(
            patched_payload,
            movie_id=9999999,
            expected_status=404
        )

        assert_not_found(resp)


@pytest.mark.parametrize('min_price,max_price,locations,genre_id',
                         [
                             (100, 1000, ['MSK'], 1),
                             (200, 2000, ['SPB'], 2)
                         ]
                         )
def test_get_movies_by_filter(
        unauthorized_movies,
        min_price,
        max_price,
        locations,
        genre_id
):
    resp = unauthorized_movies.get_movies(
        min_price=min_price,
        max_price=max_price,
        locations=locations,
        genre_id=genre_id,
    )

    body = resp.json()

    assert 'movies' in body
    assert isinstance(body['movies'], list)
    assert body['page'] == 1
    assert body['pageSize'] == 10
    assert len(body['movies']) <= 10

    for movie in body['movies']:
        assert min_price <= movie['price'] <= max_price
        assert movie['location'] in locations
        assert movie['genreId'] == genre_id
        assert movie['published'] is True

@pytest.mark.parametrize(
    'actor_fixture, expected_status',
    [
        ('super_admin', 200),
        ('common_user', 403),
        ('unauthorized_movie', 401),
    ]
)
def test_delete_movie_role_based_access(
        request,
        actor_fixture,
        expected_status,
        created_movie,
        super_admin,
):

    actor = request.getfixturevalue(actor_fixture)

    movie = Movie(api=actor.api)
    movie.id = created_movie.id

    movie.delete(expected_status=expected_status)

    if expected_status == 200:
        super_admin.api.movies.get_movie(movie.id, expected_status=404)
