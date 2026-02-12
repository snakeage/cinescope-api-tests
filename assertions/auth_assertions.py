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

def assert_login_failed(data):
    assert data, "Тело ошибки пустое"
    assert "accessToken" not in data, "Токен не должен выдаваться"
