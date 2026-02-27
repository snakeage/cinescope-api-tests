from clients.auth_api import AuthApi
from clients.movies_api import MoviesApi
from clients.user_api import UserApi


class ApiManager:
    """
    Единая точка управления API и состоянием сессии.
    """

    def __init__(self, session):
        self.session = session

        self.auth = AuthApi(session)
        self.users = UserApi(session)
        self.movies = MoviesApi(session)

    def authenticate(self, user):
        """
        Регистрирует пользователя (если нужно) и авторизует сессию.
        """
        login_data = {
            'email': user['email'],
            'password': user['_password'],
        }
        token = self.auth.login_and_get_token(login_data)

        self.session.headers.update({
            'Authorization': f'Bearer {token}'
        })

    def close_session(self):
        self.session.close()
