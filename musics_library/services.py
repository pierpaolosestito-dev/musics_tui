import json
from datetime import datetime

import requests
import getpass

from musics_library.domain import Username, Password, Music, EANCode, Genre, RecordCompany, Artist, Name, Price


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
        res = requests.post(url="http://localhost:8000/api/v1/auth/login/",json={"username":username.value\
                                                                    ,"password":password.value})
        if res.status_code != 200:
            raise ApiException("Login not successfull")
        print(res.json())
        return AuthenticatedUser(res.json()["key"],res.json()['user']['id'],res.json()['user']['username'])

    def logout(self,auth_user : AuthenticatedUser):
        res = requests.post(url="http://localhost:8000/api/v1/auth/logout/",headers={'Authorization': f'Token {auth_user.key}'})
        if res.status_code != 200:
            raise ApiException("Logout not successfull")
        return res.json()

class MusicsService:
    def fetch_musics_list(self,auth_user: AuthenticatedUser):
        res = requests.get(url="http://localhost:8000/api/v1/musics/",headers={'Authorization':f'Token {auth_user.key}'})
        if res.status_code != 200:
            raise ApiException("Request to server not successfull")
        return res.json()
    def add_music(self,auth_user: AuthenticatedUser):
        res = requests.post(url="http://localhost:8000/api/v1/musics/",headers={'Authorization':f'Token {auth_user.key}'},
                            json={
                                    "name": "Ciao",
                                    "artist": "Ciao",
                                    "record_company": "Ciao",
                                    "genre": "Reggae",
                                    "ean_code": "978020137962",
                                    #"price": "1.00",
                                    "published_by": auth_user.id
                            })
        print(res.status_code)
        if res.status_code != 201:
            raise ApiException("CD creation failed") ## todo bisogna leggere gli errori esatti e stamparli nella tui
        return res.json()

    def update_music(self,cd:Music):
        pass

    def remove_music(self,cd:Music):
        pass

login_service = LoginService()
try:
    authenticated_user = login_service.login(Username("ssdsbm28"), Password("pierfabiofabgab"))
    print(authenticated_user)
    music_service = MusicsService()
    print(music_service.add_music(authenticated_user))

except(ApiException) as e:
    print(e)



