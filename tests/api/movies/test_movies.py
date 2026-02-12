from assertions.movies_assertions import assert_movies_contract, assert_movie_contract, assert_bad_request, \
    assert_conflict, assert_not_found, assert_unauthorized, assert_forbidden
from utils.movie_payloads import MovieDataGenerator


class TestMoviesApi:
    def test_get_movies(self, api_manager):
        resp = api_manager.movies_api.get_movies()
        data = resp.json()

        assert_movies_contract(data)

    def test_get_movies_filter_by_location(self, api_manager):
        resp = api_manager.movies_api.get_movies(
            params={'locations': ['MSK']}
        )

        data = resp.json()
        movies = data['movies']
        assert movies, 'Фильтр по location вернул пустой список'

        for movie in movies:
            assert movie['location'] == 'MSK'

        assert_movies_contract(data)

    def test_get_movies_filter_by_price_range(self, api_manager):
        resp = api_manager.movies_api.get_movies(
            params={
                "minPrice": 100,
                "maxPrice": 1000
            }
        )

        data = resp.json()

        movies = data['movies']
        for movie in movies:
            assert 100 <= movie['price'] <= 1000

        assert_movies_contract(data)

    def test_get_movies_filter_by_published(self, api_manager):
        resp = api_manager.movies_api.get_movies(
            params={'published': True}
        )

        data = resp.json()

        movies = data['movies']
        for movie in movies:
            assert movie['published'] is True

        assert_movies_contract(data)

    def test_get_movies_sorted_by_created_at_desc(self, api_manager):
        resp = api_manager.movies_api.get_movies(
            params={'createdAt': 'desc'}
        )

        data = resp.json()

        movies = resp.json()['movies']
        dates = [movie['createdAt'] for movie in movies]

        assert dates == sorted(dates, reverse=True)

        assert_movies_contract(data)

    def test_get_movies_pagination(self, api_manager):
        resp = api_manager.movies_api.get_movies(
            params={'page': 1, 'pageSize': 10}
        )

        data = resp.json()

        movies = data['movies']
        assert len(movies) <= 10
        assert data['page'] == 1

        assert_movies_contract(data)

    def test_get_movies_with_invalid_param_returns_400(self, api_manager):
        resp = api_manager.movies_api.get_movies(
            params={'page': 'Invalid'},
            expected_status=400
        )

        data = resp.json()
        assert_bad_request(data)


    def test_create_movie(self, super_admin_api):
        payload = MovieDataGenerator.movie_payload()
        resp = super_admin_api.movies_api.create_movie(payload)

        data = resp.json()

        assert_movie_contract(data)

        movie_id = data['id']
        super_admin_api.movies_api.delete_movie(movie_id)

    def test_create_movie_with_invalid_name_returns_400(self, super_admin_api):
        payload = MovieDataGenerator.movie_payload(name=123)
        resp = super_admin_api.movies_api.create_movie(payload, expected_status=400)

        data = resp.json()

        assert_bad_request(data)

    def test_create_movie_with_existing_name_returns_409(self, super_admin_api, create_movie):
        original = create_movie

        payload = MovieDataGenerator.movie_payload(
            name=original['name']
        )
        resp = super_admin_api.movies_api.create_movie(
            payload, expected_status=409
        )
        data = resp.json()

        assert_conflict(data)

    def test_get_movie(self, super_admin_api, create_movie):
        movie = create_movie

        resp = super_admin_api.movies_api.get_movie(movie['id'])
        data = resp.json()

        assert_movie_contract(data)

    def test_get_movie_with_nonexisting_id_returns_404(self, super_admin_api):
        resp = super_admin_api.movies_api.get_movie(movie_id=9999999, expected_status=404)

        data = resp.json()

        assert_not_found(data)

    def test_delete_movie(self, super_admin_api, create_movie_for_delete):
        movie = create_movie_for_delete

        assert_movie_contract(movie)

        movie_id = movie['id']
        super_admin_api.movies_api.delete_movie(movie_id)

        super_admin_api.movies_api.get_movie(movie_id, expected_status=404)

    def test_delete_movie_with_nonexisting_id_returns_404(self, super_admin_api):
        resp = super_admin_api.movies_api.delete_movie(99999999, expected_status=404)
        data = resp.json()

        assert_not_found(data)

    def test_delete_movie_with_unauthorized_user_returns_401(
            self,
            api_manager,
            create_movie_for_delete
    ):
        movie_id = create_movie_for_delete['id']

        resp = api_manager.movies_api.delete_movie(
            movie_id,
            expected_status=401
        )

        data = resp.json()

        assert_unauthorized(data)

    def test_delete_movie_with_non_admin_user_returns_403(
            self,
            api_manager,
            registered_user,
            create_movie_for_delete
    ):

        api_manager.authenticate(registered_user)

        movie_id = create_movie_for_delete['id']

        resp = api_manager.movies_api.delete_movie(
            movie_id,
            expected_status=403
        )

        data = resp.json()

        assert_forbidden(data)

    def test_update_movies_name(self, super_admin_api, create_movie):
        movie = create_movie

        patched_payload = {'name': movie['name'] + '_patched'}

        resp = super_admin_api.movies_api.update_movie(
            movie['id'],
            patched_payload,
            expected_status=200
        )
        data = resp.json()
        assert_movie_contract(data)
        assert data['name'] != movie['name'], 'Название фильма не обновилось'

        updated = super_admin_api.movies_api.get_movie(movie['id']).json()
        assert updated['name'] == patched_payload['name']

    def test_update_movie_with_nonexisting_id_returns_404(
            self,
            super_admin_api,
            create_movie
        ):

        patched_payload = {'name': 'name_patched'}

        resp = super_admin_api.movies_api.update_movie(
            9999999,
            patched_payload,
            expected_status=404
        )

        data = resp.json()
        assert_not_found(data)


