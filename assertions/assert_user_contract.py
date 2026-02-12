import re

UUID_REGEX = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.IGNORECASE,
)


def assert_user_contract(data, expected_email, expected_name):
    assert isinstance(data, dict)

    assert "id" in data
    assert isinstance(data["id"], str)
    assert UUID_REGEX.match(data["id"]), "id не похож на UUID"

    assert data["email"] == expected_email
    assert data["fullName"] == expected_name

    assert isinstance(data["roles"], list)
    assert "USER" in data["roles"]

    assert isinstance(data["verified"], bool)
    assert data["verified"] is True

    assert isinstance(data["createdAt"], str)
    # проверяем, что это валидный ISO datetime
    datetime.fromisoformat(data["createdAt"].replace("Z", "+00:00"))


def assert_user_registered(register_response):
    assert register_response.status_code == 201, (
        f'Ошибка регистрации пользователя '
        f'[{register_response.status_code}]: {register_response.text}'
    )


def assert_user_logged_in(login_response):
    assert login_response.status_code == 201, (
        f'Ошибка логина пользователя '
        f'[{login_response.status_code}]: {login_response.text}'
    )


from datetime import datetime


def assert_login_contract(data, expected_email):
    # верхний уровень
    assert isinstance(data, dict)
    assert "user" in data, "В ответе отсутствует user"
    assert "accessToken" in data, "В ответе отсутствует accessToken"
    assert "expiresIn" in data, "В ответе отсутствует expiresIn"

    # accessToken
    assert isinstance(data["accessToken"], str)
    assert data["accessToken"], "accessToken пустой"

    # expiresIn
    assert isinstance(data["expiresIn"], int)
    assert data["expiresIn"] > 0, "expiresIn должен быть положительным"

    # user
    user = data["user"]
    assert isinstance(user, dict)

    assert "id" in user
    assert isinstance(user["id"], str)
    assert UUID_REGEX.match(user["id"]), "user.id не похож на UUID"

    assert user["email"] == expected_email

    assert isinstance(user["roles"], list)
    assert "USER" in user["roles"]

    # assert isinstance(user["verified"], bool)
    # assert user["verified"] is True

    # assert isinstance(user["banned"], bool)
    # assert user["banned"] is False
