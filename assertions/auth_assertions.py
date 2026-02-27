def assert_login_success(data: dict, expected_email: str):
    assert isinstance(data, dict), 'Ответ логина не является JSON-объектом'

    assert 'accessToken' in data, 'В ответе нет accessToken'
    assert data['accessToken'], 'accessToken пустой'

    assert 'expiresIn' in data, 'В ответе нет expiresIn'

    user = data.get('user')
    assert user, 'В ответе нет user'

    assert user.get('email') == expected_email, (
        f'Email пользователя не совпадает: '
        f'ожидали {expected_email}, получили {user.get("email")}'
    )

    assert 'id' in user, 'В user нет id'
    assert 'roles' in user, 'В user нет roles'


def assert_login_failed(response):
    try:
        data = response.json()
    except ValueError:
        raise AssertionError(f'Ответ не является JSON: {response.text}')

    assert isinstance(data, dict), "Ответ должен быть dict"

    assert data.get("statusCode") == 401
    assert isinstance(data.get("message"), str)
    assert isinstance(data.get("error"), str)

    assert "accessToken" not in data, "Токен не должен выдаваться"

    return data

def assert_get_user_forbidden(response):
    try:
        data = response.json()
    except ValueError:
        raise AssertionError(f'Ответ не является JSON: {response.text}')

    assert data, 'Отсутствует тело ответа'
    assert isinstance(data, dict), 'Тело ответа должно быть dict'

    for field in ('message', 'error', 'statusCode'):
        assert field in data, f'Отсутствует поле {field} в ответе'

    assert data['statusCode'] == 403

    return data