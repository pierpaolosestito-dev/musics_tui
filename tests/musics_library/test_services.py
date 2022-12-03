from unittest.mock import patch

import dotenv
import pytest
import os
import requests
@pytest.fixture
def load_dotenv():
    yield dotenv.load_dotenv()

def test_dotenv(load_dotenv):
    assert os.getenv('ROOT_ENDPOINT') == "http://localhost:8000"
    assert os.getenv('MUSIC_ENDPOINT') == "http://localhost:8000/api/v1/musics/"
    assert os.getenv('AUTH_ENDPOINT') == "http://localhost:8000/api/v1/auth/"

# #
# # > def test_url(requests_mock):
# # ...     requests_mock.get('http://test.com', text='data')
# # ...     assert 'data' == requests.get('http://test.com').text
# def test_musics_get_status_code_200(requests_mock):
#     requests_mock.get(os.getenv('MUSIC_ENDPOINT')+"a")
#     assert requests.get(os.getenv('MUSIC_ENDPOINT')+"a").status_code == 200
#
# def test_auth_login(requests_mock):
#     requests_mock.post(os.getenv('AUTH_ENDPOINT')+"login/",json={"username":"ssdsbm","password":"ssdsbm"})
#     assert requests.post(os.getenv('AUTH_ENDPOINT')+"login/",json={"username":"ssdsbm","password":"ssdsbm"}).status_code == 200
#
# def test_auth_logout(requests_mock):
#     requests_mock.post(os.getenv('AUTH_ENDPOINT') + "login/",text="accessiblekey")
#     key = requests.post(os.getenv('AUTH_ENDPOINT') + "login/").text
#
#     requests_mock.post(os.getenv('AUTH_ENDPOINT') + "logout/", headers={'Authorization': f"Token {key}"})
#     assert requests.post(os.getenv('AUTH_ENDPOINT') + "logout/", headers={'Authorization': f"Token {key}"}).status_code == 200
#
