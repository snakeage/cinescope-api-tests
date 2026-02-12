def assert_movies_contract(data):
    assert 'movies' in data, 'В ответе нет поля movies'
    assert isinstance(data['movies'], list), 'movies должен быть списком'
    assert len(data['movies']) > 0, 'Список movies пуст'

    movie = data['movies'][0]
    for field in ('id', 'name', 'price', 'genreId'):
        assert field in movie, f'Отсутствует поле {field}'

def assert_movie_contract(data):
    assert data, 'Тело ответа отсутсвует'
    assert isinstance(data, dict), 'Ответ должен быть dict'

    for field in ('name', 'price', 'location'):
        assert field in data, f'Отсутствует поле {field}'

def assert_bad_request(data):
    assert data["statusCode"] == 400
    assert data["error"] == "Bad Request"
    assert data["message"]

def assert_conflict(data):
    assert data["statusCode"] == 409
    assert data["error"] == "Conflict"
    assert "уже существует" in data["message"]

def assert_not_found(data):
    assert data["statusCode"] == 404
    assert data["error"] == "Not Found"
    assert "не найден" in data["message"]

def assert_unauthorized(data):
    assert data["statusCode"] == 401
    assert data["message"]

def assert_forbidden(data):
    assert data["statusCode"] == 403
    assert data["message"]