

import dotenv
import pytest
import os

from musics_library.domain import Username, ID
from musics_library.services import AuthenticatedUser
@pytest.fixture
def load_dotenv():
    yield dotenv.load_dotenv()

def test_dotenv(load_dotenv):
    assert os.getenv('ROOT_ENDPOINT') == "http://localhost:8000"
    assert os.getenv('MUSIC_ENDPOINT') == "http://localhost:8000/api/v1/musics/"
    assert os.getenv('AUTH_ENDPOINT') == "http://localhost:8000/api/v1/auth/"


def test_authenticated_user_is_singleton():
    a = AuthenticatedUser('eyJhbGciOiJIUzI1NiIsInR5c',ID(1),Username("ssdsbm28"))
    b = AuthenticatedUser()
    assert id(a) == id(b)
    assert a.key == b.key
    assert a.id == b.id
    assert a.username == b.username