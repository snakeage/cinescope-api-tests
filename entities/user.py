from clients.api_manager import ApiManager


class User:
    def __init__(
            self,
            email: str,
            password: str,
            roles: list[str],
            api: ApiManager,

    ):
        self.email = email
        self.password = password
        self.roles = roles
        self.api = api
        self.id = None
        self.token = None

    @property
    def creds(self):
        return {
            'email': self.email,
            'password': self.password
        }

    def register(self, payload):
        response = self.api.auth.register_user(payload)
        body = response.json()
        self.id = body['id']
        return response

    def login(self, creds=None, expected_status=200):
        if creds is None:
            creds = self.creds

        return self.api.auth.login(creds, expected_status=expected_status)

    def authenticate(self):
        token = self.api.auth.login_and_get_token(self.creds)

        self.api.session.headers.update({
            'Authorization': f'Bearer {token}'
        })

        self.token = token

        return token

    def get_user(self, locator, expected_status=200):
        return self.api.users.get_user(
            locator,
            expected_status=expected_status
        )

    def create_user(self, payload, expected_status=201):
        return self.api.users.create_user(payload, expected_status=expected_status)

    def delete(self):
        return self.api.users.delete_user(self.id)
