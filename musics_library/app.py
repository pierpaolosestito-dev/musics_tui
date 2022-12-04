from musics_library.domain import Username, Email, Password
from musics_library.menu import Menu,Entry,Description
from typing import Callable,Any

from musics_library.services import AuthenticationService


class App:


    def __init__(self):
        self.login_service = AuthenticationService()
        self.menu = Menu.Builder(Description("Music Library"),auto_select=lambda:self.__print_welcome())\
             \
            .with_entry(Entry.create('1', 'Add CD', on_selected=lambda: print("Ciao"))) \
            .with_entry(Entry.create('2', 'Remove CD', on_selected=lambda: print("Ciao"))) \
            .with_entry(Entry.create('3', 'Update a CD', on_selected=lambda: print("Ciao"))) \
            .with_entry(Entry.create('4', 'Get all CDs by Publisher', on_selected=lambda: print("Ciao"))) \
            .with_entry(Entry.create('5', 'Get all CDs by CD Name', on_selected=lambda: print("Ciao"))) \
            .with_entry(Entry.create('6', 'Get all CDs by Artist', on_selected=lambda: print("Ciao"))) \
            .with_entry(Entry.create('7', 'Get all CDs', on_selected=lambda: print("Ciao"))) \
            .with_entry(Entry.create('8', 'Login', on_selected=lambda: self.__read_user())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print('Bye'),is_exit=True))\
            .build()
        #self.__music_library = MusicLibrary()
        #PSEUDOCODICE MUSIC LIBRARY
        #def __init__():
        # self.music_service = MusicService()
        # self.music_by_artist...bla bla bla
        #
        # def musics():
        # questo chiamata music_service.fetch_list() e ritorna la lista.
        # def

    def __print_welcome(self)->None:
        print("Welcome")
        print("If you want to register an account into Music Library you can go here, {link}")


    def __read_user(self):
        user = self.__read('Username', Username)
        email = self.__read('Email', Email)
        password = self.__read('Password', Password)
        return user,email,password
    def __login(self):
        pass
        #user = self.__read_user()
        #LoginService -> login() SALVA LA KEY IN QUESTO MOMENTO,logout()
        #MusicService - CRUD -> fetchMusics(),update_music(),delete_music(),add_music()
        #MusicByArtistService - GET -> fetchByArtist(artist_name:Artist)
        #MusicByPublishersService - GET -> fetchByPublishers(publisher_name:Publisher)
        #MusicByCDNameService - GET -> fetchByCDName(cd_name : Name)

    @staticmethod
    def __read(prompt:str,builder:Callable)->Any:
        while True:
            try:
                line = input(f'{prompt}: ')
                res = builder(line.strip())
                return res
            except:
                print("Error")

    def __run(self)->None:
        try:
            self.__print_welcome()
        except:
            print('Continuing with an empty list of vehicles...')
        self.menu.run()

    def run(self)->None:
        try:
            self.__run()
        except(Exception) as a:
            print(a)
            print('Panic error!')