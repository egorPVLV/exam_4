# Глобальные константы

BASE_URL = "https://api.dev-cinescope.coconutqa.ru"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

LOGIN_ENDPOINT = "/login"
REGISTER_ENDPOINT = "/register"
MOVIES_ENDPOINT = "/movies"
GENRES_ENDPOINT = "/genres"
REVIEW_ENDPOINT = "/reviews"

NAME = "api1@gmail.com"
PASSWORD = "asdqwe123Q"
ADMIN_USER_ID = "a76b8bf9-af13-45bb-b200-b9db86db26d3"  # Из логов

REGISTER_DATA = {
    "email": "newuser@example.com",
    "fullName": "New User",
    "password": "12345678Aa",
    "passwordRepeat": "12345678Aa"
}

LOGIN_DATA = {
    "email": NAME,
    "password": PASSWORD
}

CREATE_USER_DATA = {
    "email": "admin@example.com",
    "fullName": "Admin User",
    "password": "SecurePass123!",
    "verified": True,
    "banned": False
}

EDIT_USER_DATA = {
    "roles": ["USER", "ADMIN"],
    "verified": True,
    "banned": False
}
