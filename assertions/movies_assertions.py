def assert_movies_contract(response):
    try:
        data = response.json()
    except ValueError:
        raise AssertionError(f'Ответ не является JSON: {response.text}')

    assert data, "Response body is empty"
    assert isinstance(data, dict), "Response must be dict"

    assert "movies" in data, "Response missing 'movies'"
    assert isinstance(data["movies"], list), "'movies' must be list"
    assert data["movies"], "'movies' list is empty"

    required_fields = ("id", "name", "price", "genreId")

    for i, movie in enumerate(data["movies"]):

        assert isinstance(movie, dict), f"Movie #{i} is not dict"

        for field in required_fields:
            assert field in movie, f"Movie #{i} missing field '{field}'"

        assert isinstance(movie["id"], int), f"Movie #{i} id must be int"
        assert isinstance(movie["name"], str), f"Movie #{i} name must be str"
        assert isinstance(movie["price"], (int, float)), f"Movie #{i} price must be number"

    return data


def assert_movie_contract(response):
    try:
        data = response.json()
    except ValueError:
        raise AssertionError(f'Ответ не является JSON: {response.text}')

    assert data, "Response body is empty"
    assert isinstance(data, dict), "Response must be dict"

    required_fields = (
        "id",
        "name",
        "price",
        "location",
        "createdAt",
    )

    for field in required_fields:
        assert field in data, f"Missing field '{field}'"

    assert isinstance(data["id"], int)
    assert isinstance(data["name"], str)
    assert isinstance(data["price"], (int, float))
    assert isinstance(data["location"], str)

    return data

def assert_error_contract(response, status_code, error=None):
    try:
        data = response.json()
    except ValueError:
        raise AssertionError(f'Ответ не является JSON: {response.text}')

    assert isinstance(data, dict), "Response must be dict"

    assert data.get("statusCode") == status_code, \
        f"Expected {status_code}, got {data.get('statusCode')}"

    if error:
        assert data.get("error") == error

    assert data.get("message"), "Error message is empty"

    return data


def assert_bad_request(response):
    assert_error_contract(response, 400, "Bad Request")


def assert_conflict(data):
    assert_error_contract(data, 409, "Conflict")


def assert_not_found(data):
    assert_error_contract(data, 404, "Not Found")


def assert_unauthorized(data):
    assert_error_contract(data, 401)


def assert_forbidden(data):
    assert_error_contract(data, 403)
