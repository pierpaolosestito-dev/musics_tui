from valid8 import ValidationError

from musics_library.domain import Password, Name, Artist, RecordCompany, Genre, Username, Email, EANCode
import pytest


#NAME
def test_empty_name_raises_exception():
    with pytest.raises(ValidationError):
        Name("")

def test_name_length_of_51_raises_exception():
    with pytest.raises(ValidationError):
        Name("A"*51)

def test_name_accepts_some_symbols_like_space_minus_and_comma():
    name_with_symbols = ['Blink!','AC-DC','Jelly, The Fish!',"@AM"]
    for name in name_with_symbols:
        assert Name(name)

def test_name_str():
    assert str(Name("SSDSBM")) == "SSDSBM"

#ARTIST
def test_empty_artist_name_raises_exception():
    with pytest.raises(ValidationError):
        Artist("")

def test_artist_name_of_length_51_raises_exception():
    with pytest.raises(ValidationError):
        Artist("A"*51)

def test_artist_name_accepts_some_symbols_like_space_minus_and_comma():
    name_with_symbols = ['Blink!','AC-DC','Jelly, The Fish!',"@AM"]
    for name in name_with_symbols:
        assert Artist(name)

def test_artist_name_str():
    assert str(Artist("SSDSBM")) == "SSDSBM"

#RECORDCOMPANY
def test_empty_record_company_raises_exception():
    with pytest.raises(ValidationError):
        RecordCompany("")

def test_record_company_of_length_51_raises_exception():
    with pytest.raises(ValidationError):
        RecordCompany("A"*51)

def test_record_company_accepts_some_symbols_like_space_minus_and_comma():
    name_with_symbols = ['Blink!','AC-DC','Jelly, The Fish!',"@AM","#MusiCEnTerTainMEnt"]
    for name in name_with_symbols:
        assert RecordCompany(name)

def test_record_company_str():
    assert str(RecordCompany("SSDSBM - Music Entertainment")) == "SSDSBM - Music Entertainment"
#GENRE
def test_empty_genre_raises_exception():
    with pytest.raises(ValidationError):
        Genre("")
def test_genre_of_length_26_raises_exception():
    with pytest.raises(ValidationError):
        Genre("A"*26)

def test_genre_accepts_only_whitespaces():
    wrong_values = ["Rock!","Rock-n-Roll","Jazz!@","Blues1"]
    for wrong in wrong_values:
        with pytest.raises(ValidationError):
            Genre(wrong)

    correct_values = ["Rock","Rock n Roll","Folk","Jazz","Blues","Heavy Metal"]
    for correct in correct_values:
        assert Genre(correct)

def test_genre_first_letter_is_upper():
    with pytest.raises(ValidationError):
        Genre("rock")
    assert Genre("Rock")

@pytest.mark.parametrize("ean_code", [("978020137962"), ("1845678901001")])
def test_ean_code(ean_code):
    assert EANCode(ean_code)


def test_genre_str():
    assert str(Genre("Rock")) == "Rock"

#USERNAME
def test_empty_username_raises_exception():
    with pytest.raises(ValidationError):
        Username("")

def test_username_of_length_151_raises_exception():
    with pytest.raises(ValidationError):
        Username("A"*151)

def test_username_only_accepts_characters_and_numbers():
    wrong_values = ["u'@-sername","u\sername123","u!ser"]
    for wrong in wrong_values:
        with pytest.raises(ValidationError):
            Username(wrong)
    correct_values = ['username123','Ricky1',"ssdsbm14"]
    for correct in correct_values:
        assert Username(correct)

#EMAIL
def test_empty_email_raises_exception():
    with pytest.raises(ValidationError):
        Email("")

def test_email_of_length_151_raises_exception():
    with pytest.raises(ValidationError):
        Email("p"*146+"@a.it")

def test_email_format():
    wrong_values = ["wrong_email@it","anotherwrongemail.it"]
    for wrong in wrong_values:
        with pytest.raises(ValidationError):
            Email(wrong)
    correct_values = ["correct_email@gmail.com","correct.email@libero.it","correct12_email@yahoo.it"]
    for correct in correct_values:
        assert Email(correct)

def test_email_str():
    assert str(Email("ssdsbm@gmail.com")) == "ssdsbm@gmail.com"



#PASSWORD
@pytest.mark.parametrize("wrong_passwords", [("A"), ("aa@"), ("Aa "), ("A-!@"), ("Aaaaa"),("Aaa aa"), ("Aaaaaaa")])
def test_password_has_min_length_of_8(wrong_passwords):
    with pytest.raises(ValueError):
        Password(wrong_passwords)
    assert Password("Abcd!-@.")

def test_password_length_of_129_raises_exception():
    with pytest.raises(ValueError):
        Password("A"*128+"a")

def test_password_with_spaces_raises_exception():
    with pytest.raises(ValueError):
        Password("A"*6+" "+"a")