import re
from datetime import datetime

from constants.roles import Roles

UUID_REGEX = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.IGNORECASE,
)


def assert_user_contract(response, expected_email, expected_name):
    try:
        data = response.json()
    except ValueError:
        raise AssertionError(f"Ответ не является JSON: {response.text}")

    assert isinstance(data, dict), "Ответ должен быть dict"

    user_id = data.get("id")
    assert user_id, "Отсутствует id"
    assert isinstance(user_id, str)
    assert UUID_REGEX.match(user_id), "id не похож на UUID"

    assert data.get("email") == expected_email
    assert data.get("fullName") == expected_name

    roles = data.get("roles")
    assert isinstance(roles, list), "roles должен быть list"
    assert "USER" in roles

    assert isinstance(data.get("verified"), bool)
    assert data["verified"] is True

    created_at = data.get("createdAt")
    assert isinstance(created_at, str)
    datetime.fromisoformat(created_at.replace("Z", "+00:00"))

    return data


def assert_login_contract(response, expected_email):
    try:
        data = response.json()
    except ValueError:
        raise AssertionError(f"Ответ не является JSON: {response.text}")

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

    return data

def assert_user_created(response, expected_payload, expected_roles=None):
    data = assert_user_response(response)

    for field in ("email", "fullName", "verified"):
        assert data[field] == expected_payload[field], (
            f"{field}: ожидали {expected_payload[field]}, "
            f"получили {data[field]}"
        )

    if expected_roles is not None:
        assert data["roles"] == expected_roles

    return data

def assert_user_response(response):
    try:
        data = response.json()
    except ValueError:
        raise AssertionError(f"Ответ не является JSON: {response.text}")

    assert isinstance(data, dict), "Тело ответа должно быть dict"

    required_fields = (
        "id", "email", "fullName",
        "createdAt", "verified", "banned", "roles"
    )

    for field in required_fields:
        assert data.get(field) is not None, f"Отсутствует поле {field}"

    datetime.fromisoformat(data["createdAt"].replace("Z", "+00:00"))

    return data