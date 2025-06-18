from api.auth_api import AuthAPI
from api.user_api import UserAPI
from api.movies_api import MoviesAPI

class ApiManager:
    """
    Класс для управления API-классами с единой HTTP-сессией.
    """
    def __init__(self, session):
        """
        Инициализация ApiManager.
        :param session: HTTP-сессия, используемая всеми API-классами.
        """
        self.session = session
        self.auth_api = AuthAPI(session)
        self.user_api = UserAPI(session)
        self.movies_api = MoviesAPI(session)

        # Авторизация
        login_data = {"email": "api1@gmail.com", "password": "asdqwe123Q"}
        response = self.auth_api.login_user(login_data)
        assert response.status_code == 200
        token = response.json().get("accessToken")

        # Применяем токен ко всем последующим запросам
        session.headers.update({"Authorization": f"Bearer {token}"})
