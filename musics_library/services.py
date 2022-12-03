
import requests
from musics_library.domain import Username, Password, Music, EANCode, Genre, RecordCompany, Artist, Name, Price
from dotenv import load_dotenv
import os

load_dotenv()

music_endpoint = os.getenv('MUSIC_ENDPOINT')
auth_endpoint = os.getenv('AUTH_ENDPOINT')

class AuthenticatedUser:
    def __init__(self, key: str,id:int,username:str):
        self.key = key
        self.id = id
        self.username = username

    def __str__(self):
        return self.key + " " + str(self.id)
class ApiException(Exception):
    pass

class LoginService:
    #User
    def login(self,username:Username,password:Password):
        res = requests.post(url=auth_endpoint+"login/",json={"username":username.value\
                                                                    ,"password":password.value})
        if res.status_code != 200:
            raise ApiException("Login not successfull")
        print(res.json())
        return AuthenticatedUser(res.json()["key"],res.json()['user']['id'],res.json()['user']['username'])

    def logout(self,auth_user : AuthenticatedUser):
        res = requests.post(url=auth_endpoint+"logout/",headers={'Authorization': f'Token {auth_user.key}'})
        if res.status_code != 200:
            raise ApiException("Logout not successfull")
        return res.json()

class MusicsService:
    def fetch_musics_list(self,auth_user: AuthenticatedUser): #TODO Qua potremmo anche toglierlo auth_user perché le GET le facciamo fare anche a chi non è in possesso di un token.
        res = requests.get(url=music_endpoint,headers={'Authorization':f'Token {auth_user.key}'})
        if res.status_code != 200:
            raise ApiException("Request to server not successfull")
        return res.json() #TODO Deve essere una lista di Music

    def add_music(self,cd:Music,auth_user: AuthenticatedUser):
        dict = cd.toDict()
        dict['published_by'] = auth_user.id
        res = requests.post(url=music_endpoint,headers={'Authorization':f'Token {auth_user.key}'},
                            json=dict)
        if res.status_code != 201:
            raise ApiException("CD creation failed") ## todo bisogna leggere gli errori esatti e stamparli nella tui
        return res.json()

    def update_music(self,cd:Music,auth_user:AuthenticatedUser):
        pass

    def remove_music(self,cd:Music,auth_user:AuthenticatedUser):
        pass


class MusicsByArtistService():
    #http://localhost:8000/api/v1/musics/byartist?artist=ciccio
    def fetch_musics_by_artist_list(self,artist_name:Artist,auth_user: AuthenticatedUser): #TODO Qua potremmo anche toglierlo auth_user perché le GET le facciamo fare anche a chi non è in possesso di un token.
        res = requests.get(url=music_endpoint+"byartist?artist="+artist_name.value,headers={'Authorization':f'Token {auth_user.key}'})
        if res.status_code != 200:
            raise ApiException("Request to server not successfull")
        return res.json()

class MusicsByPublishedByService():
    # http://localhost:8000/api/v1/musics/by_published_by?published_by=ciccio
    def fetch_musics_by_published_by_list(self,published_by:Username,auth_user:AuthenticatedUser):
        res = requests.get(url=music_endpoint+"by_published_by?published_by=" + published_by.value,
                           headers={'Authorization': f'Token {auth_user.key}'})
        if res.status_code != 200:
            raise ApiException("Request to server not successfull")
        return res.json()

class MusicsByNameService():
    #http://localhost:8000/api/v1/musics/byname?name=ciccio
    def fetch_musics_by_name_list(self,cd_name:Name,auth_user:AuthenticatedUser):
        res = requests.get(url=music_endpoint+"byname?name=" + cd_name.value,
                           headers={'Authorization': f'Token {auth_user.key}'})
        if res.status_code != 200:
            raise ApiException("Request to server not successfull")
        return res.json()



# login_service = LoginService()
# try:
#     authenticated_user = login_service.login(Username("ssdsbm28"), Password("pierfabiofabgab"))
#     print(authenticated_user)
#     music_service = MusicsService()
#     cd = Music(Name("Ciao"),Artist("Ciao"),RecordCompany("Ciao"),Genre("Ciao"),EANCode("978020137962"),Username("ssdsbm28"),Price.create(15,50),datetime.now(),datetime.now())
#     print(music_service.add_music(cd,authenticated_user))
#
# except(ApiException) as e:
#     print(e)
