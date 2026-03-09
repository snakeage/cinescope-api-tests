from models.errors_models import ErrorResponse


def assert_login_failed(response):
    try:
        data = ErrorResponse.model_validate(response.json())
    except ValueError:
        raise AssertionError(f'Ответ не является JSON: {response.text}')

    assert data.status_code == 401
    assert isinstance(data.message, str)
    assert data.message

    assert 'accessToken' not in response.json(), 'Токен не должен выдаваться'

    return data


def assert_get_user_forbidden(response):
    try:
        data = ErrorResponse.model_validate(response.json())
    except ValueError:
        raise AssertionError(f'Ответ не является JSON: {response.text}')

    assert data.status_code == 403
    assert isinstance(data.message, str)
    assert data.message

    return data
