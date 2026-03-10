import allure
import pytest

from assertions.movies_assertions import (
    assert_bad_request,
    assert_conflict,
    assert_forbidden,
    assert_not_found,
    assert_unauthorized,
)
from db.queries import get_movies_by_ids
from entities.movie import Movie
from models.movie_models import MovieResponse, MoviesListResponse
from utils.movie_payloads import MovieDataGenerator

pytestmark = pytest.mark.api


class TestMoviesApi:
    @allure.title('Get movies returns a non-empty list')
    @allure.description(
        'Check that public movies endpoint returns a valid non-empty list of movies.'
    )
    @pytest.mark.smoke_stable
    @pytest.mark.regression
    def test_get_movies(self, unauthorized_movies):
        with allure.step('Request movies list'):
            data = unauthorized_movies.get_movies(response_model=MoviesListResponse)

        with allure.step('Validate movies response'):
            assert isinstance(data.movies, list)
            assert data.movies

    @allure.title('Get movies filter by location')
    @allure.description('Check that movies endpoint returns only movies from requested locations.')
    @pytest.mark.regression
    def test_get_movies_filter_by_location(self, unauthorized_movies):
        location = ['MSK']
        with allure.step(f'Request movies filter by location: {location}'):
            data = unauthorized_movies.get_movies(
                locations=location, response_model=MoviesListResponse
            )

        with allure.step('Validate filtered movies list'):
            movies = data.movies
            assert movies, 'Фильтр по location вернул пустой список'

            for movie in movies:
                assert movie.location == 'MSK'

    @allure.title('Get movies filter by price range')
    @allure.description(
        'Check that movies endpoint returns only movies from requested price range.'
    )
    @pytest.mark.regression
    def test_get_movies_filter_by_price_range(self, unauthorized_movies):
        with allure.step('Request movies filtered by price range'):
            data = unauthorized_movies.get_movies(
                min_price=100, max_price=1000, response_model=MoviesListResponse
            )
        with allure.step('Validate filtered movies list'):
            for movie in data.movies:
                assert 100 <= movie.price <= 1000

    @allure.title('Get movies filter by published')
    @allure.description(
        'Check that movies endpoint returns only movies from requested filter published.'
    )
    @pytest.mark.regression
    def test_get_movies_filter_by_published(self, unauthorized_movies):
        with allure.step('Request movies filtered by published=true'):
            data = unauthorized_movies.get_movies(published=True, response_model=MoviesListResponse)

        with allure.step('Validate filtered movies list'):
            for movie in data.movies:
                assert movie.published is True

    @allure.title('Get movies sorted by createdAt in descending order')
    @allure.description(
        'Checks that movies endpoint returns movies sorted by createdAt in descending order.'
    )
    @pytest.mark.regression
    def test_get_movies_sorted_by_created_at_desc(self, unauthorized_movies):
        with allure.step('Request movies sorted by createdAt descending'):
            data = unauthorized_movies.get_movies(
                created_at='desc', response_model=MoviesListResponse
            )

        with allure.step('Validate movies are sorted by createdAt descending'):
            dates = [movie.created_at for movie in data.movies]

            assert dates == sorted(dates, reverse=True)

    @allure.title('Get movies pagination returns requested page size')
    @allure.description('Checks that movies endpoint returns expected page and page size values.')
    @pytest.mark.regression
    def test_get_movies_pagination(self, unauthorized_movies):
        with allure.step('Request first page with page size 10'):
            data = unauthorized_movies.get_movies(
                page=1, page_size=10, response_model=MoviesListResponse
            )

        with allure.step('Validate pagination response'):
            assert len(data.movies) <= 10
            assert data.page == 1
            assert data.page_size == 10

    @allure.title('Get movies with invalid page returns 400')
    @allure.description('Checks that movies endpoint returns 400 for invalid page value.')
    @pytest.mark.negative
    @pytest.mark.regression
    def test_get_movies_with_invalid_param_returns_400(self, unauthorized_movies):
        with allure.step('Send request with invalid page parameter'):
            resp = unauthorized_movies.get_movies(page='Invalid', expected_status=400)

        with allure.step('Validate bad request response'):
            assert_bad_request(resp)

    @allure.title('Create movie')
    @allure.description('Checks that movies endpoint creates a movie.')
    @pytest.mark.smoke_integration
    @pytest.mark.regression
    def test_create_movie(self, movie, movie_data):
        with allure.step('Send request with correct payload'):
            created = movie.create(movie_data, response_model=MovieResponse)

        with allure.step('Validate request response'):
            assert created.id is not None
            assert created.name == movie_data['name']

    @allure.title('Create movie with invalid type of movie name')
    @allure.description('Checks that movies endpoint returns 400 for invalid name type.')
    @pytest.mark.negative
    @pytest.mark.regression
    def test_create_movie_with_invalid_name_returns_400(self, movie):
        with allure.step('Send request with invalid name type'):
            payload = MovieDataGenerator.movie_payload(name=123)
            resp = movie.create(payload, expected_status=400)

        with allure.step('Validate bad request response'):
            assert_bad_request(resp)

    @allure.title('Create movie with existing name returns 409')
    @allure.description(
        'Checks that movies endpoint returns conflict when creating a movie with an existing name.'
    )
    @pytest.mark.negative
    @pytest.mark.regression
    def test_create_movie_with_existing_name_returns_409(self, movie, created_movie):
        with allure.step('Prepare payload with existing movie name'):
            payload = MovieDataGenerator.movie_payload(name=created_movie.name)

        with allure.step('Send create movie request with duplicate name'):
            resp = movie.create(payload, expected_status=409)

        with allure.step('Validate conflict response'):
            assert_conflict(resp)

    @allure.title('Get movie by id returns movie details')
    @allure.description('Checks that created movie can be retrieved by id.')
    @pytest.mark.smoke_integration
    @pytest.mark.regression
    def test_get_movie(self, created_movie):
        with allure.step('Request movie by id'):
            got = created_movie.get(response_model=MovieResponse)

        with allure.step('Validate movie response'):
            assert got.id == created_movie.id

    @allure.title('Get movie with non-existing id returns 404')
    @allure.description('Checks that movies endpoint returns 404 for non-existing movie id.')
    @pytest.mark.negative
    @pytest.mark.regression
    def test_get_movie_with_nonexisting_id_returns_404(self, movie):
        with allure.step('Request non-existing movie by id'):
            resp = movie.get(movie_id=9999999, expected_status=404)

        with allure.step('Validate not found response'):
            assert_not_found(resp)

    @allure.title('Delete movie makes it unavailable')
    @allure.description('Checks that deleted movie becomes unavailable for further retrieval.')
    @pytest.mark.workflow
    @pytest.mark.regression
    def test_delete_movie(self, created_movie):
        with allure.step('Delete created movie'):
            deleted = created_movie.delete(response_model=MovieResponse)

        with allure.step('Validate delete response'):
            assert deleted.id == created_movie.id

        with allure.step('Verify deleted movie is not found'):
            created_movie.get(expected_status=404)

    @allure.title('Delete non-existing movie returns 404')
    @allure.description('Checks that deleting a non-existing movie returns 404.')
    @pytest.mark.negative
    @pytest.mark.regression
    @pytest.mark.slow
    def test_delete_movie_with_nonexisting_id_returns_404(self, created_movie):
        with allure.step('Delete non-existing movie by id'):
            resp = created_movie.delete(movie_id=99999999, expected_status=404)

        with allure.step('Validate not found response'):
            assert_not_found(resp)

    @allure.title('Delete movie without authorization returns 401')
    @allure.description('Checks that unauthorized user cannot delete a movie.')
    @pytest.mark.negative
    @pytest.mark.regression
    def test_delete_movie_with_unauthorized_user_returns_401(self, unauthorized_movie):
        with allure.step('Delete movie without authorization'):
            resp = unauthorized_movie.delete(expected_status=401)

        with allure.step('Validate unauthorized response'):
            assert_unauthorized(resp)

    @allure.title('Delete movie by non-admin user returns 403')
    @allure.description('Checks that non-admin user cannot delete a movie.')
    @pytest.mark.negative
    @pytest.mark.regression
    @pytest.mark.slow
    def test_delete_movie_with_non_admin_user_returns_403(self, registered_movie):
        with allure.step('Delete movie as non-admin user'):
            resp = registered_movie.delete(expected_status=403)

        with allure.step('Validate forbidden response'):
            assert_forbidden(resp)

    @allure.title('Update movie name returns updated movie')
    @allure.description('Checks that movie name can be updated and response contains new name.')
    @pytest.mark.workflow
    @pytest.mark.regression
    def test_update_movies_name(self, created_movie):
        with allure.step('Prepare patched movie name'):
            old_name = created_movie.name

            patched_payload = {'name': old_name + '_patched'}

        with allure.step('Update movie name'):
            updated = created_movie.update(
                patched_payload, expected_status=200, response_model=MovieResponse
            )

        with allure.step('Validate updated movie response'):
            assert updated.name != old_name, 'Название фильма не обновилось'
            assert updated.name == patched_payload['name']

    @allure.title('Update non-existing movie returns 404')
    @allure.description('Checks that updating a non-existing movie returns 404.')
    @pytest.mark.negative
    @pytest.mark.regression
    def test_update_movie_with_nonexisting_id_returns_404(self, movie):
        with allure.step('Prepare update payload for non-existing movie'):
            patched_payload = {'name': 'name_patched'}

        with allure.step('Update non-existing movie by id'):
            resp = movie.update(patched_payload, movie_id=9999999, expected_status=404)

        with allure.step('Validate not found response'):
            assert_not_found(resp)


@allure.title('Get movies by combined filters')
@allure.description(
    'Checks that movies endpoint applies combined filters for price, location and genre.'
)
@pytest.mark.regression
@pytest.mark.parametrize(
    'min_price,max_price,locations,genre_id', [(100, 1000, ['MSK'], 1), (200, 2000, ['SPB'], 2)]
)
def test_get_movies_by_filter(unauthorized_movies, min_price, max_price, locations, genre_id):
    with allure.step(
        'Request movies with filters: '
        f'prices {min_price}-{max_price}, locations {locations}, genre {genre_id}'
    ):
        body = unauthorized_movies.get_movies(
            min_price=min_price,
            max_price=max_price,
            locations=locations,
            genre_id=genre_id,
            response_model=MoviesListResponse,
        )

    with allure.step('Validate filtered movies response'):
        assert isinstance(body.movies, list)
        assert body.page == 1
        assert body.page_size == 10
        assert len(body.movies) <= 10

        for movie in body.movies:
            assert min_price <= movie.price <= max_price
            assert movie.location in locations
            assert movie.genre_id == genre_id
            assert movie.published is True


@allure.title('Delete movie respects role-based access')
@allure.description(
    'Checks that delete movie action returns expected result for different user roles.'
)
@pytest.mark.workflow
@pytest.mark.regression
@pytest.mark.parametrize(
    'actor_fixture, expected_status',
    [
        ('super_admin', 200),
        ('common_user', 403),
        ('unauthorized_movie', 401),
    ],
)
def test_delete_movie_role_based_access(
    request,
    actor_fixture,
    expected_status,
    created_movie,
    super_admin,
):
    with allure.step(f'Get actor from fixture: {actor_fixture}'):
        actor = request.getfixturevalue(actor_fixture)

    with allure.step('Prepare movie entity for delete request'):
        movie = Movie(api=actor.api)
        movie.id = created_movie.id

    if expected_status == 200:
        with allure.step('Delete movie as allowed actor'):
            deleted = movie.delete(
                expected_status=200,
                response_model=MovieResponse,
            )

        with allure.step('Validate successful delete response'):
            assert deleted.id == created_movie.id

        with allure.step('Verify deleted movie is not found'):
            super_admin.api.movies.get_movie(
                movie.id,
                expected_status=404,
            )
    else:
        with allure.step(f'Delete movie with expected status {expected_status}'):
            movie.delete(expected_status=expected_status)


@allure.title('Published movies in API are consistent with DB')
@allure.description(
    'Checks that published movies returned by API are marked as published in database.'
)
@pytest.mark.db
@pytest.mark.regression
def test_api_movies_published_consistent_with_db(unauthorized_movies, db_session):
    with allure.step('Request published movies from API'):
        api_resp = unauthorized_movies.get_movies(
            published=True, page=1, page_size=20, response_model=MoviesListResponse
        )

    with allure.step('Load same movies from DB'):
        api_ids = [movie.id for movie in api_resp.movies]
        db_rows = get_movies_by_ids(db_session, api_ids)
        db_map = {row['id']: row['published'] for row in db_rows}

    with allure.step('Validate API and DB consistency'):
        assert len(db_map) == len(api_ids), 'Часть фильмов из API не найдена в БД'
        for movie_id in api_ids:
            assert db_map[movie_id] is True, f'Фильм {movie_id} в БД не published'


@allure.title('Get movies filters by locations')
@allure.description('Checks that movies endpoint returns only movies from requested locations.')
@pytest.mark.regression
@pytest.mark.parametrize(
    'locations',
    [['MSK'], ['SPB'], ['MSK', 'SPB']],
    ids=['location: MSK', 'location: SPB', 'location: [MSK, SPB]'],
)
def test_get_movies_location_filter(unauthorized_movies, locations):
    with allure.step(f'Request movies filtered by locations: {locations}'):
        data = unauthorized_movies.get_movies(
            locations=locations,
            response_model=MoviesListResponse,
        )

    with allure.step('Validate filtered movies list'):
        movies = data.movies

        for movie in movies:
            assert movie.location in locations

        assert movies
