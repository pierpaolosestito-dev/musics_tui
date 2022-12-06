from datetime import datetime

from musics_library.console import Console, MusicConsole
from musics_library.domain import Username, Email, Password, Name, Artist, RecordCompany, Genre, EANCode, Price, Music, \
    ID
from musics_library.menu import Menu,Entry,Description
from typing import Callable,Any

from musics_library.services import AuthenticationService, AuthenticatedUser, MusicLibrary

from rich.console import Console
from rich.prompt import Prompt,Confirm
from rich.table import Table
class App:
    def __init__(self):
        self.login_service = AuthenticationService()
        self.authenticated_user = None
        self.music_library = MusicLibrary()
        self.menu = Menu.Builder(Description("Music Library"),auto_select=lambda:print())\
             \
            .with_entry(Entry.create('1', 'Add CD', on_selected=lambda: self.__add_music())) \
            .with_entry(Entry.create('2', 'Remove CD', on_selected=lambda: self.__remove_music())) \
            .with_entry(Entry.create('3', 'Update a CD', on_selected=lambda: self.__update_music())) \
            .with_entry(Entry.create('4', 'Get all CDs by Publisher', on_selected=lambda: self.__print_musics_by_published_by())) \
            .with_entry(Entry.create('5', 'Get all CDs by CD Name', on_selected=lambda: self.__print_musics_by_cd_name())) \
            .with_entry(Entry.create('6', 'Get all CDs by Artist', on_selected=lambda: self.__print_musics_by_artist())) \
            .with_entry(Entry.create('7', 'Get all CDs', on_selected=lambda: self.__print_musics())) \
            .with_entry(Entry.create('8', 'Login', on_selected=lambda: self.__login(),visibility_or_not=lambda: print())) \
            .with_entry(Entry.create('9', 'Logout', on_selected=lambda: self.__logout(),visibility_or_not=lambda:print())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print('Music Library says you Goodbye!'),is_exit=True))\
            .build()

        self.console = Console()


    def __print_welcome(self)->None:
        print("Welcome")
        print("If you want to register an account into Music Library you can go here, {link}")

    def __add_music(self):
        music = Music(*self.__read_add_cd())
        y_or_n = Confirm.ask("Are you sure?")
        if y_or_n:
            self.music_library.add_music(music,self.authenticated_user)
        else:
            self.console.print("Music not added")

    def __update_music(self):
        id = self.__read('ID',ID.parse)
        cd = self.music_library.music(id)
        self.__create_and_print_table_with_single_cd(cd)
        self.__read_for_update('Name',cd.name.value,Name)

    def __remove_music(self):
        id = self.__read('ID', ID.parse)
        cd = self.music_library.music(id)

        self.__create_and_print_table_with_single_cd(cd)

        y_or_n = Confirm.ask("Are you sure that you want delete this record?")
        if y_or_n:
            self.music_library.remove_music(id,self.authenticated_user)
        else:
            self.console.print("Record will not be deleted.")

    def __create_and_print_table_with_single_cd(self, cd):
        table = Table()
        columns = ['#', 'NAME', 'ARTIST', 'RECORD COMPANY', 'GENRE', 'EANCODE', 'PRICE', 'PUBLISHED BY',
                   'CREATED AT', 'UPDATED AT']
        for col in columns:
            table.add_column(col)
        table.add_row(str(cd.id.value), cd.name.value, cd.artist.value, cd.record_company.value, cd.genre.value,
                      cd.ean_code.value, str(cd.price),
                      cd.published_by.value, str(cd.created_at), str(cd.updated_at))
        self.console.print(table)

    def __create_and_print_table_with_list_of_cd(self,musics):
        table = Table()
        columns = ['#', 'NAME', 'ARTIST', 'RECORD COMPANY', 'GENRE', 'EANCODE', 'PRICE', 'PUBLISHED BY',
                   'CREATED AT', 'UPDATED AT']
        for col in columns:
            table.add_column(col)


        for cd in musics:
            table.add_row(str(cd.id.value), cd.name.value, cd.artist.value, cd.record_company.value, cd.genre.value,
                          cd.ean_code.value, str(cd.price),
                          cd.published_by.value, str(cd.created_at), str(cd.updated_at))
        self.console.print(table)

    def __print_musics_by_artist(self):
        artist = self.__read('Artist',Artist)
        musics = self.music_library.musics_by_artist(artist)
        self.__create_and_print_table_with_list_of_cd(musics)


    def __print_musics_by_published_by(self):
        published_by = self.__read('Username', Username)
        musics = self.music_library.musics_by_published_by(published_by)
        self.__create_and_print_table_with_list_of_cd(musics)

    def __print_musics_by_cd_name(self):
        cd_name = self.__read('CD Name', Name)
        musics = self.music_library.musics_by_published_by(cd_name)
        self.__create_and_print_table_with_list_of_cd(musics)

    def __print_musics(self)->None:
        musics = self.music_library.musics()
        self.__create_and_print_table_with_list_of_cd(musics)

    def __read_add_cd(self):
        #ID fittizio, created_at e updated_at fittizi fin quando non abbiamo una sol più intelligente.
        name = self.__read("Name", Name)
        artist = self.__read("Artist", Artist)
        record_company = self.__read("Record Company", RecordCompany)
        genre = self.__read("Genre", Genre)
        #ean_code = self.__read("EANCode", EANCode)
        ean_code = EANCode("978020137962")
        price = self.__read("Price", Price.parse)
        return name, artist, record_company, genre, ean_code, price


    def __read_user(self):
        user = self.__read('Username', Username)
        password = self.__read('Password', Password)
        return user,password

    def __login(self):
        username,password = self.__read_user()
        self.authenticated_user = self.login_service.login(username,password)
        print("Welcome " + self.authenticated_user.username.value)

    def __logout(self):
        y_or_n = Confirm.ask("Are you sure that you want to logout?")
        if y_or_n:
            self.login_service.logout(self.authenticated_user)

    @staticmethod
    def __read(prompt:str,builder:Callable)->Any:
        while True:
            try:
                line = Prompt.ask(f'{prompt} ')
                res = builder(line.strip())
                return res
            except:
                print("Error")

    @staticmethod
    def __read_for_update(prompt: str,default:str, builder: Callable) -> Any:
        while True:
            try:
                line = Prompt.ask(f'{prompt} ',default=default)
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

App().run()