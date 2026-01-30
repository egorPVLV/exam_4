from api.auth_api import AuthAPI
from api.user_api import UserAPI
from api.movies_api import MoviesAPI

class ApiManager:
    def __init__(self, session, base_url: str=None):
        self.session = session
        self.user_api = UserAPI(session, base_url=base_url)
        self.movies_api = MoviesAPI(session, base_url=base_url)
