from models.errors_models import ErrorResponse


def assert_error_contract(response, status_code, error=None):
    try:
        data = ErrorResponse.model_validate(response.json())
    except ValueError:
        raise AssertionError(f'Ответ не является JSON: {response.text}')

    assert data.status_code == status_code, f'Expected {status_code}, got {data.status_code}'

    if error is not None:
        assert data.error == error

    assert data.message, 'Error message is empty'

    return data


def assert_bad_request(response):
    assert_error_contract(response, 400, 'Bad Request')


def assert_conflict(data):
    assert_error_contract(data, 409, 'Conflict')


def assert_not_found(data):
    assert_error_contract(data, 404, 'Not Found')


def assert_unauthorized(data):
    assert_error_contract(data, 401)


def assert_forbidden(data):
    assert_error_contract(data, 403)
