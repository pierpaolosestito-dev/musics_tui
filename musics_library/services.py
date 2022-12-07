from dataclasses import dataclass,field
from datetime import datetime
from typing import List

import requests
from dateutil.parser import parser
from typeguard import typechecked

from musics_library.domain import Username, Password, Music, EANCode, Genre, RecordCompany, Artist, Name, Price, ID
from dotenv import load_dotenv
import os
from dateutil import parser

load_dotenv()

music_endpoint = os.getenv('MUSIC_ENDPOINT')
auth_endpoint = os.getenv('AUTH_ENDPOINT')

class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args,**kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class AuthenticatedUser(metaclass=SingletonMeta):
    def __init__(self, key: str,id:ID,username:Username):
        self.key = key
        self.id = id
        self.username = username

    def __str__(self):
        return self.key + " " + str(self.id.value)


class ApiException(Exception):
    pass

CONNECTION_ERROR = "Check your network connection or retry later."
LOGIN_ERROR = "Login not successfull"
LOGOUT_ERROR = "Logout not successfull"
GET_TO_SERVER_FAILED_ERROR = "The desired operation has failed. Try later"
POST_PUT_DELETE_ERROR = GET_TO_SERVER_FAILED_ERROR + "or check your data"
class AuthenticationService:
    #User
    def login(self,username:Username,password:Password):
        res = requests.post(url=auth_endpoint+"login/",json={"username":username.value\
                                                                    ,"password":password.value})
        if res.status_code != 200:
            raise ApiException(LOGIN_ERROR)
        return AuthenticatedUser(res.json()["key"],ID(res.json()['user']['id']),Username(res.json()['user']['username']))

    def logout(self,auth_user : AuthenticatedUser):
        res = requests.post(url=auth_endpoint+"logout/",headers={'Authorization': f'Token {auth_user.key}'})
        if res.status_code != 200:
            raise ApiException(LOGOUT_ERROR)
        return res.json()


class MusicsService:
    #musicslibrary.domain import Music
    authenticated_user = AuthenticatedUser

    def __to_dict(self, cd:Music):  # toDict attuale è stato creato per far funzionare la POST. #requests.put(url,json=cd.toDict()) NO ES POSIBLE. nella Delete invece, dobbiamo solo spostarci ID
            return {
                "name": cd.name.value,
                "artist": cd.artist.value,
                "record_company": cd.record_company.value,
                "genre": cd.genre.value,
                "ean_code": cd.ean_code.value,
                "price": str(cd.price)
            }


    def fetch_musics_list(self):#Lista di Musics -> un Array, o un List della libreria typing #TODO MIGLIORARE return e gestione errori
        try:
            res = requests.get(url=music_endpoint)
        except:
            raise ApiException(CONNECTION_ERROR)
        if res.status_code != 200:
            raise ApiException(GET_TO_SERVER_FAILED_ERROR)
        cds = []
        for i in res.json():
            created_at = parser.parse(i['created_at'])
            updated_at = parser.parse(i['updated_at'])
            cd = Music(\
                ID(i['id']),\
                Name(i['name']),\
                Artist(i['artist']),\
                RecordCompany(i['record_company']),\
                Genre(i['genre']),\
                EANCode(i['ean_code']), \
                Username(i['user']), \
                Price.parse(i['price']),\
                created_at,\
                updated_at
                )
            cds.append(cd)


        return cds #TODO Deve essere una lista di Music



    def fetch_music_detail(self,cd_id:ID):
        try:
            res = requests.get(url=music_endpoint+str(cd_id.value)+"/")
        except:
            raise ApiException(CONNECTION_ERROR)
        if res.status_code != 200:
            raise ApiException(GET_TO_SERVER_FAILED_ERROR)
        i = res.json()
        created_at = parser.parse(i['created_at'])
        updated_at = parser.parse(i['updated_at'])
        cd = Music( \
            ID(i['id']), \
            Name(i['name']), \
            Artist(i['artist']), \
            RecordCompany(i['record_company']), \
            Genre(i['genre']), \
            EANCode(i['ean_code']), \
            Username(i['user']), \
            Price.parse(i['price']), \
            created_at, \
            updated_at
        )
        return cd

    def add_music(self,cd:Music,auth_user: AuthenticatedUser):
        dict = self.__to_dict(cd)
        dict['published_by'] = auth_user.id.value

        try:
            res = requests.post(url=music_endpoint,headers={'Authorization':f'Token {auth_user.key}'},
                            json=dict)
        except:
            raise ApiException(CONNECTION_ERROR)
        if res.status_code != 201:
            raise ApiException(GET_TO_SERVER_FAILED_ERROR) ## todo bisogna leggere gli errori esatti e stamparli nella tui
        i = res.json()
        created_at = parser.parse(i['created_at'])
        updated_at = parser.parse(i['updated_at'])
        cd2 = Music( \
            ID(i['id']), \
            Name(i['name']), \
            Artist(i['artist']), \
            RecordCompany(i['record_company']), \
            Genre(i['genre']), \
            EANCode(i['ean_code']), \
            Username(i['user']), \
            Price.parse(i['price']), \
            created_at, \
            updated_at
        )
        return cd2


    def update_music(self,cd:Music,auth_user : AuthenticatedUser):
        dict = self.__to_dict(cd)
        dict['id'] = cd.id.value
        dict['published_by'] = auth_user.id
        try:
            res = requests.put(url=music_endpoint+str(cd.id.value)+"/",headers={'Authorization':f'Token {auth_user.key}'},
                           json=dict)
        except:
            raise ApiException(CONNECTION_ERROR)

        if res.status_code != 200:
            raise ApiException(POST_PUT_DELETE_ERROR)
        return True

    def remove_music(self,cd_id:ID,auth_user:AuthenticatedUser):
        try:
            res = requests.delete(url=music_endpoint+str(cd_id.value)+"/",headers={'Authorization':f'Token {auth_user.key}'})
        except:
            raise ApiException(CONNECTION_ERROR)
        if res.status_code != 204:
            raise ApiException(POST_PUT_DELETE_ERROR)
        return True


class MusicsByArtistService():
    #http://localhost:8000/api/v1/musics/byartist?artist=ciccio
    def fetch_musics_by_artist_list(self,artist_name:Artist): #TODO Qua potremmo anche toglierlo auth_user perché le GET le facciamo fare anche a chi non è in possesso di un token.
        try:
            res = requests.get(url=music_endpoint+"byartist?artist="+artist_name.value)
        except:
            raise ApiException(CONNECTION_ERROR)
        if res.status_code != 200:
            raise ApiException(GET_TO_SERVER_FAILED_ERROR)
        return res.json()

class MusicsByPublishedByService():
    # http://localhost:8000/api/v1/musics/by_published_by?published_by=ciccio
    def fetch_musics_by_published_by_list(self,published_by:Username):

        try:
            res = requests.get(url=music_endpoint+"by_published_by?published_by=" + published_by.value)
        except:
            raise ApiException(CONNECTION_ERROR)

        if res.status_code != 200:
            raise ApiException(GET_TO_SERVER_FAILED_ERROR)
        return res.json()

class MusicsByNameService():
    #http://localhost:8000/api/v1/musics/byname?name=ciccio
    def fetch_musics_by_name_list(self,cd_name:Name):
        try:
            res = requests.get(url=music_endpoint+"byname?name=" + cd_name.value)
        except:
            raise ApiException(CONNECTION_ERROR)
        if res.status_code != 200:
            raise ApiException(GET_TO_SERVER_FAILED_ERROR)
        return res.json()

@typechecked
@dataclass(frozen=True)
class MusicLibrary:


    musics_service: MusicsService = field(default_factory=MusicsService,init=False)
    musics_by_artists_service : MusicsByArtistService = field(default_factory=MusicsByArtistService,init=False)
    musics_by_published_by_service : MusicsByPublishedByService = field(default_factory=MusicsByPublishedByService,init=False)
    musics_by_cd_name_service : MusicsByNameService = field(default_factory=MusicsByNameService,init=False)


    def musics(self) -> 'List[Music]':
        return self.musics_service.fetch_musics_list()

    def music(self,id:ID) -> 'Music':
        return self.musics_service.fetch_music_detail(id)

    def add_music(self,music:Music,auth_user:AuthenticatedUser) -> 'Music':
        return self.musics_service.add_music(music,auth_user)

    def update_music(self,music:Music,auth_user:AuthenticatedUser) -> bool:
        return self.musics_service.update_music(music,auth_user)

    def remove_music(self,id:ID,auth_user:AuthenticatedUser) -> bool:
        return self.musics_service.remove_music(id,auth_user)

    def musics_by_artist(self,artist:Artist)->'List[Music]':
        return self.musics_by_artists_service.fetch_musics_by_artist_list(artist)

    def musics_by_published_by(self,published_by:Username)->'List[Music]':
        return self.musics_by_published_by_service.fetch_musics_by_published_by_list(published_by)

    def musics_by_cd_name(self,cd_name:Name)->'List[Music]':
        return self.musics_by_cd_name_service.fetch_musics_by_name_list(cd_name)



# login_service = AuthenticationService()
# try:
#       authenticated_user = login_service.login(Username("ssdsbm"), Password("ssdsbm"))
#       print(authenticated_user)
#       music_service = MusicsService()
#
#       #cd = Music(Name("DaTUI"), Artist("Ciao"), RecordCompany("Ciao"), Genre("Ciao"), EANCode("978020137962"),Price.create(15, 50))
#       print(music_service.remove_musica(ID(49),authenticated_user))
#
# except(ApiException) as e:
#       print(e)

