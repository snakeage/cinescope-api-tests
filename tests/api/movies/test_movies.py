import pytest

from assertions.movies_assertions import (
    assert_bad_request,
    assert_conflict,
    assert_forbidden,
    assert_not_found,
    assert_unauthorized,
)
from entities.movie import Movie
from models.movie_models import MovieResponse, MoviesListResponse
from utils.movie_payloads import MovieDataGenerator


class TestMoviesApi:
    def test_get_movies(self, unauthorized_movies):
        data = unauthorized_movies.get_movies(response_model=MoviesListResponse)

        assert isinstance(data.movies, list)

    def test_get_movies_filter_by_location(self, unauthorized_movies):
        data = unauthorized_movies.get_movies(
            locations=['MSK'],
            response_model=MoviesListResponse
        )

        movies = data.movies
        assert movies, 'Фильтр по location вернул пустой список'

        for movie in movies:
            assert movie.location == 'MSK'

    def test_get_movies_filter_by_price_range(self, unauthorized_movies):
        data = unauthorized_movies.get_movies(
            min_price=100,
            max_price=1000,
            response_model=MoviesListResponse
        )

        for movie in data.movies:
            assert 100 <= movie.price <= 1000

    def test_get_movies_filter_by_published(self, unauthorized_movies):
        data = unauthorized_movies.get_movies(
            published=True,
            response_model=MoviesListResponse
        )

        for movie in data.movies:
            assert movie.published is True

    def test_get_movies_sorted_by_created_at_desc(self, unauthorized_movies):
        data = unauthorized_movies.get_movies(
            created_at='desc',
            response_model=MoviesListResponse
        )

        dates = [movie.created_at for movie in data.movies]

        assert dates == sorted(dates, reverse=True)

    def test_get_movies_pagination(self, unauthorized_movies):
        data = unauthorized_movies.get_movies(
            page=1,
            page_size=10,
            response_model=MoviesListResponse
        )

        assert len(data.movies) <= 10
        assert data.page == 1
        assert data.page_size == 10

    def test_get_movies_with_invalid_param_returns_400(self, unauthorized_movies):
        resp = unauthorized_movies.get_movies(
            page='Invalid',
            expected_status=400
        )

        assert_bad_request(resp)

    def test_create_movie(self, movie, movie_data):
        created = movie.create(
            movie_data,
            response_model=MovieResponse
        )

        assert created.id is not None
        assert created.name == movie_data['name']

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
        got = created_movie.get(response_model=MovieResponse)

        assert got.id == created_movie.id

    def test_get_movie_with_nonexisting_id_returns_404(self, movie):
        resp = movie.get(movie_id=9999999, expected_status=404)

        assert_not_found(resp)

    def test_delete_movie(self, created_movie):
        deleted = created_movie.delete(response_model=MovieResponse)

        assert deleted.id == created_movie.id

        created_movie.get(expected_status=404)

    @pytest.mark.slow
    def test_delete_movie_with_nonexisting_id_returns_404(self, created_movie):
        resp = created_movie.delete(movie_id=99999999, expected_status=404)

        assert_not_found(resp)

    def test_delete_movie_with_unauthorized_user_returns_401(
            self,
            unauthorized_movie
    ):

        resp = unauthorized_movie.delete(expected_status=401)

        assert_unauthorized(resp)

    @pytest.mark.slow
    def test_delete_movie_with_non_admin_user_returns_403(
            self,
            registered_movie
    ):

        resp = registered_movie.delete(expected_status=403)

        assert_forbidden(resp)

    def test_update_movies_name(self, created_movie):
        old_name = created_movie.name

        patched_payload = {'name': old_name + '_patched'}

        updated = created_movie.update(
            patched_payload,
            expected_status=200,
            response_model=MovieResponse
        )

        assert updated.name != old_name, 'Название фильма не обновилось'
        assert updated.name == patched_payload['name']

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
    body = unauthorized_movies.get_movies(
        min_price=min_price,
        max_price=max_price,
        locations=locations,
        genre_id=genre_id,
        response_model=MoviesListResponse
    )

    assert isinstance(body.movies, list)
    assert body.page == 1
    assert body.page_size == 10
    assert len(body.movies) <= 10

    for movie in body.movies:
        assert min_price <= movie.price <= max_price
        assert movie.location in locations
        assert movie.genre_id == genre_id
        assert movie.published is True


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
