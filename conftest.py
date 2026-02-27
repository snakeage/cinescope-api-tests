import pytest
import requests

from clients.api_manager import ApiManager
from constants.roles import Roles
from entities.movie import Movie
from entities.user import User
from resources.user_creds import SuperAdminCreds
from utils.movie_payloads import MovieDataGenerator
from utils.user_payloads import generate_admin_user_payload


@pytest.fixture
def user_session():
    sessions = []

    def _create():
        session = requests.Session()
        api = ApiManager(session)
        sessions.append(api)
        return api

    yield _create

    for api in sessions:
        api.close_session()


@pytest.fixture
def api(user_session):
    return user_session()


@pytest.fixture
def auth_api(api):
    return api.auth


@pytest.fixture
def super_admin(user_session):
    api = user_session()

    super_admin = User(
        email=SuperAdminCreds.USERNAME,
        password=SuperAdminCreds.PASSWORD,
        roles=[Roles.SUPER_ADMIN.value],
        api=api,
    )

    super_admin.authenticate()

    return super_admin


@pytest.fixture
def user_factory(user_session, super_admin):
    created_users = []

    def _create_user(role: Roles):

        api = user_session()

        payload, password = generate_admin_user_payload()

        response = super_admin.api.users.create_user(payload)

        created_user = response.json()

        user = User(
            email=payload['email'],
            password=password,
            roles=[role.value],
            api=api
        )

        user.id = created_user['id']
        user.full_name = created_user['fullName']
        user.verified = created_user['verified']
        user.authenticate()

        created_users.append(user)

        return user

    yield _create_user

    for user in created_users:
        try:
            super_admin.api.users.delete_user(user.id)
        except Exception:
            pass


@pytest.fixture
def common_user(user_factory):
    return user_factory(Roles.USER)


@pytest.fixture
def unauthorized_api(user_session):
    return user_session()


@pytest.fixture
def unauthorized_movie(unauthorized_api, created_movie, super_admin):
    movie = Movie(api=unauthorized_api)
    movie.id = created_movie.id
    movie.data = created_movie.data

    yield movie

    if movie.id:
        admin_movie = Movie(api=super_admin.api)
        admin_movie.id = movie.id
        admin_movie.delete(expected_status=[200, 404])


@pytest.fixture
def unauthorized_movies(unauthorized_api):
    movies = Movie(api=unauthorized_api)

    return movies


@pytest.fixture
def registered_movie(common_user, created_movie, super_admin):
    movie = Movie(api=common_user.api)
    movie.id = created_movie.id
    movie.data = created_movie.data

    yield movie

    if movie.id:
        admin_movie = Movie(api=super_admin.api)
        admin_movie.id = movie.id
        admin_movie.delete(expected_status=[200, 404])


@pytest.fixture
def movie_data():
    return MovieDataGenerator.movie_payload()


@pytest.fixture
def movie(super_admin):
    movie = Movie(api=super_admin.api)

    yield movie

    if movie.id:
        movie.delete(expected_status=[200, 404])


@pytest.fixture
def created_movie(movie, movie_data):
    movie.create(movie_data)

    return movie
