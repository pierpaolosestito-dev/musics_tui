import os
from dataclasses import dataclass, field
from typing import List

import requests
from dotenv import load_dotenv
from typeguard import typechecked

import musics_library.mappers as mappers
from musics_library.domain import Username, Password, CD, Artist, Name, ID
from musics_library.exceptions import ApiException

load_dotenv()

music_endpoint = os.getenv('MUSIC_ENDPOINT')
auth_endpoint = os.getenv('AUTH_ENDPOINT')





class AuthenticatedUser():
    def __init__(self, key: str, id: ID, username: Username,is_superuser: bool,is_publisher: bool):
        self.key = key
        self.id = id
        self.username = username
        self.is_authorized = is_superuser or is_publisher

    def __str__(self):
        return self.key + " " + str(self.id.value) + " " + str(self.is_authorized)



CONNECTION_ERROR = "Check your network connection or retry later."
LOGIN_ERROR = "Login not successfull"
LOGOUT_ERROR = "Logout not successfull"
GET_ERROR = "The desired operation has failed. Try later"
GET_DETAIL_ERROR = "Music object doesn't exists."
POST_ERROR = "MUSIC ADD FAILED"
PUT_ERROR = "MUSIC UPDATE FAILED"
DELETE_ERROR = "MUSIC DELETE FAILED"
PERMISSION_ADD_ERROR = "You must be publisher, register on website."
PERMISSION_ERROR = "You must be the publisher of this record."

class AuthenticationService:
    # User
    def login(self, username: Username, password: Password):
        try:
            res = requests.post(url=auth_endpoint + "login/", json={"username": username.value \
                , "password": password.value})
        except:
            raise ApiException(CONNECTION_ERROR)
        if res.status_code != 200:
            raise ApiException(LOGIN_ERROR)

        authenticated_user = mappers.AuthenticatedUserMapper.map_auth_user(res)
        return authenticated_user

    def logout(self, auth_user: AuthenticatedUser):
        try:
            res = requests.post(url=auth_endpoint + "logout/", headers={'Authorization': f'Token {auth_user.key}'})
        except:
            raise ApiException(CONNECTION_ERROR)
        if res.status_code != 200:
            raise ApiException(LOGOUT_ERROR)
        return res.json()


class CDService:
    # musicslibrary.domain import Music
    authenticated_user = AuthenticatedUser

    def __to_dict(self, cd: CD):
        return {
            "name": cd.name.value,
            "artist": cd.artist.value,
            "record_company": cd.record_company.value,
            "genre": cd.genre.value,
            "ean_code": cd.ean_code.value,
            "price": str(cd.price)
        }

    def fetch_cd_list(
            self):  # Lista di Musics -> un Array, o un List della libreria typing #TODO MIGLIORARE return e gestione errori
        try:
            res = requests.get(url=music_endpoint)
        except:
            raise ApiException(CONNECTION_ERROR)
        if res.status_code != 200:
            raise ApiException(GET_ERROR)
        cds = []
        for i in res.json():
            cd = mappers.CDMapper.map_cd(i)
            cds.append(cd)

        return cds  # TODO Deve essere una lista di Music

    def fetch_cd_detail(self, cd_id: ID):
        try:
            res = requests.get(url=music_endpoint + str(cd_id.value) + "/")
        except:
            raise ApiException(CONNECTION_ERROR)
        if res.status_code != 200:
            raise ApiException(GET_DETAIL_ERROR)

        i = res.json()
        cd = mappers.CDMapper.map_cd(i)
        return cd

    def add_cd(self, cd: CD, auth_user: AuthenticatedUser):
        dict = self.__to_dict(cd)
        dict['published_by'] = auth_user.id.value

        try:
            res = requests.post(url=music_endpoint, headers={'Authorization': f'Token {auth_user.key}'},
                                json=dict)
        except:
            raise ApiException(CONNECTION_ERROR)
        if res.status_code == 403:
            raise ApiException(PERMISSION_ADD_ERROR)
        if res.status_code != 201:
            raise ApiException(POST_ERROR)  ## todo bisogna leggere gli errori esatti e stamparli nella tui
        cd2 = mappers.CDMapper.map_cd(res.json())
        return cd2

    def update_cd(self, cd: CD, auth_user: AuthenticatedUser):
        dict = self.__to_dict(cd)
        dict['id'] = cd.id.value
        dict['published_by'] = auth_user.id.value
        try:

            res = requests.put(url=music_endpoint + str(cd.id) + "/",
                               headers={'Authorization': f'Token {auth_user.key}'},
                               json=dict)
        except:
            raise ApiException(CONNECTION_ERROR)

        if res.status_code == 403:
            raise ApiException(PERMISSION_ERROR)
        if res.status_code != 200:
            raise ApiException(PUT_ERROR)
        return True

    def remove_cd(self, cd_id: ID, auth_user: AuthenticatedUser):
        try:
            res = requests.delete(url=music_endpoint + str(cd_id.value) + "/",
                                  headers={'Authorization': f'Token {auth_user.key}'})
        except:
            raise ApiException(CONNECTION_ERROR)
        if res.status_code == 403:
            raise ApiException(PERMISSION_ERROR)
        if res.status_code != 204:
            raise ApiException(DELETE_ERROR)
        return True


class CDByArtistService():
    # http://localhost:8000/api/v1/musics/byartist?artist=ciccio
    def fetch_cd_by_artist_list(self,
                                artist_name: Artist):  # TODO Qua potremmo anche toglierlo auth_user perché le GET le facciamo fare anche a chi non è in possesso di un token.
        try:
            res = requests.get(url=music_endpoint + "byartist?artist=" + artist_name.value)
        except:
            raise ApiException(CONNECTION_ERROR)
        if res.status_code != 200:
            raise ApiException(GET_ERROR)
        cds = []
        for i in res.json():
            cd = mappers.CDMapper.map_cd(i)
            cds.append(cd)
        return cds


class CDByPublishedByService():
    # http://localhost:8000/api/v1/musics/by_published_by?published_by=ciccio
    def fetch_cd_by_published_by_list(self, published_by: Username):
        try:
            res = requests.get(url=music_endpoint + "by_published_by?publishedby=" + published_by.value)
        except:
            raise ApiException(CONNECTION_ERROR)
        if res.status_code != 200:
            raise ApiException(GET_ERROR)
        cds = []
        for i in res.json():
            cd = mappers.CDMapper.map_cd(i)
            cds.append(cd)
        return cds


class CDByNameService():
    # http://localhost:8000/api/v1/musics/byname?name=ciccio
    def fetch_musics_by_name_list(self, cd_name: Name):
        try:
            res = requests.get(url=music_endpoint + "byname?name=" + cd_name.value)
        except:
            raise ApiException(CONNECTION_ERROR)
        if res.status_code != 200:
            raise ApiException(GET_ERROR)
        cds = []
        for i in res.json():
            cd = mappers.CDMapper.map_cd(i)
            cds.append(cd)
        return cds


@typechecked
@dataclass(frozen=True)
class CDLibrary:
    cd_service: CDService = field(default_factory=CDService, init=False)
    cd_by_artists_service: CDByArtistService = field(default_factory=CDByArtistService, init=False)
    cd_by_published_by_service: CDByPublishedByService = field(default_factory=CDByPublishedByService,
                                                               init=False)
    cd_by_name_service: CDByNameService = field(default_factory=CDByNameService, init=False)

    def musics(self) -> 'List[CD]':
        return self.cd_service.fetch_cd_list()

    def music(self, id: ID) -> 'CD':
        return self.cd_service.fetch_cd_detail(id)

    def add_music(self, music: CD, auth_user: AuthenticatedUser) -> 'CD':
        return self.cd_service.add_cd(music, auth_user)

    def update_music(self, music: CD, auth_user: AuthenticatedUser) -> bool:
        return self.cd_service.update_cd(music, auth_user)

    def remove_music(self, id: ID, auth_user: AuthenticatedUser) -> bool:
        return self.cd_service.remove_cd(id, auth_user)

    def musics_by_artist(self, artist: Artist) -> 'List[CD]':
        return self.cd_by_artists_service.fetch_cd_by_artist_list(artist)

    def musics_by_published_by(self, published_by: Username) -> 'List[CD]':
        return self.cd_by_published_by_service.fetch_cd_by_published_by_list(published_by)

    def musics_by_cd_name(self, cd_name: Name) -> 'List[CD]':
        return self.cd_by_name_service.fetch_musics_by_name_list(cd_name)
