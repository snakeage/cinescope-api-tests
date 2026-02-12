import pytest
import requests

from clients.api_manager import ApiManager
from utils.data_generator import DataGenerator
from utils.movie_payloads import MovieDataGenerator


@pytest.fixture(scope='session')
def session():
    s = requests.Session()
    yield s
    s.close()


@pytest.fixture(scope='session')
def api_manager(session):
    return ApiManager(session)


@pytest.fixture
def test_user():
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        'email': random_email,
        'fullName': random_name,
        'password': random_password,
        'passwordRepeat': random_password,
        'roles': ['USER']
    }.copy()


@pytest.fixture
def authorized_api(api_manager, registered_user):
    api_manager.authenticate(registered_user)
    return api_manager


@pytest.fixture
def registered_user(api_manager, test_user):
    resp = api_manager.auth_api.register_user(test_user)
    user = resp.json()

    user['_password'] = test_user['password']

    yield user
    api_manager.authenticate(user)
    api_manager.user_api.delete_user(user['id'])

@pytest.fixture
def movie_data():
    return MovieDataGenerator.movie_payload().copy()

@pytest.fixture(scope="session")
def super_admin_credentials():
    return {
        "email": "api1@gmail.com",
        "password": "asdqwe123Q"
    }

@pytest.fixture
def super_admin_api(super_admin_credentials):
    session = requests.Session()
    manager = ApiManager(session)

    token = manager.auth_api.login_and_get_token(super_admin_credentials)

    session.headers.update({
        'Authorization': f'Bearer {token}'
    })

    return manager

@pytest.fixture
def create_movie(super_admin_api):
    payload = MovieDataGenerator.movie_payload()
    resp = super_admin_api.movies_api.create_movie(payload)

    movie = resp.json()

    yield movie

    movie_id = movie['id']
    super_admin_api.movies_api.delete_movie(movie_id)

@pytest.fixture
def create_movie_for_delete(super_admin_api):
    payload = MovieDataGenerator.movie_payload()
    resp = super_admin_api.movies_api.create_movie(payload)

    movie = resp.json()

    return movie