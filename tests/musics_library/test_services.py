from datetime import datetime
from unittest.mock import Mock, patch

import dotenv
import pytest
import os

from musics_library.domain import Username, ID, Price, EANCode, Genre, RecordCompany, Artist, Name, Music
from musics_library.services import AuthenticatedUser, MusicsService, MusicsByPublishedByService, MusicsByArtistService, \
    ApiException, MusicsByNameService


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

def test_str_authenticated_user():
    assert str(AuthenticatedUser('eyJhbGciOiJIUzI1NiIsInR5c',ID(1),Username("ssdsbm28"))) == "eyJhbGciOiJIUzI1NiIsInR5c 1"

import requests

def test_musics_service_fetch_musics_list(requests_mock):
    requests_mock.get("http://localhost:8000/api/v1/musics/",json="")
    ms = MusicsService()
    resp = ms.fetch_musics_list()
    assert resp != None

def test_musics_service_by_publisher_fetch_musics_list(requests_mock):
    published_by = Username("ssdsbm")
    requests_mock.get("http://localhost:8000/api/v1/musics/by_published_by?published_by="+published_by.value, json="")
    ms = MusicsByPublishedByService()
    resp = ms.fetch_musics_by_published_by_list(published_by)
    assert resp != None

def test_musics_service_by_artist_fetch_musics_list(requests_mock):
    artist = Artist("ssdsbm")
    requests_mock.get("http://localhost:8000/api/v1/musics/byartist?artist="+artist.value, json="")
    ms = MusicsByArtistService()
    resp = ms.fetch_musics_by_artist_list(artist)
    assert resp != None

def test_musics_service_by_cd_name_fetch_musics_list(requests_mock):
        cd_name = Name("ssdsbm")
        requests_mock.get("http://localhost:8000/api/v1/musics/byname?name=" + cd_name.value,
                          json="")
        ms = MusicsByNameService()
        resp = ms.fetch_musics_by_name_list(cd_name)
        assert resp != None
def test_musics_services_wrong_url_raises_api_exception(requests_mock):
    with pytest.raises(ApiException):
        requests_mock.get("http://localhost:8000/api/v1/musics/wrong_path", json="")
        ms = MusicsService()
        resp = ms.fetch_musics_list()

def test_musics_services_by_artist_wrong_url_raises_api_exception(requests_mock):
    with pytest.raises(ApiException):
        artist = Artist("ssdsbm")
        requests_mock.get("http://localhost:8000/api/v1/musics/byarattist?artist=" + artist.value, json="")
        ms = MusicsByArtistService()
        resp = ms.fetch_musics_by_artist_list(artist)

def test_musics_services_by_published_by_wrong_url_raises_api_exception(requests_mock):
    with pytest.raises(ApiException):
        published_by = Username("ssdsbm")
        requests_mock.get("http://localhost:8000/api/v1/musics/by_published_byyyy?published_by=" + published_by.value,
                          json="")
        ms = MusicsByPublishedByService()
        resp = ms.fetch_musics_by_published_by_list(published_by)

def test_musics_services_by_cd_name_wrong_url_raises_api_exception(requests_mock):
    with pytest.raises(ApiException):
        cd_name = Name("ssdsbm")
        requests_mock.get("http://localhost:8000/api/v1/musics/bynamee?published_by=" + cd_name.value,
                          json="")
        ms = MusicsByNameService()
        resp = ms.fetch_musics_by_name_list(cd_name)