import os

from dotenv import load_dotenv

load_dotenv()

AUTH_BASE_URL = os.getenv('AUTH_BASE_URL', 'https://auth.dev-cinescope.coconutqa.ru').rstrip('/')
API_BASE_URL = os.getenv('API_BASE_URL', 'https://api.dev-cinescope.coconutqa.ru').rstrip('/')

HEADERS = {'Content-Type': 'application/json', 'Accept': 'application/json'}

LOGIN_ENDPOINT = '/login'
REGISTER_ENDPOINT = '/register'

MOVIES = '/movies'
