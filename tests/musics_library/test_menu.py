from unittest.mock import Mock, patch

import pytest
from valid8 import ValidationError

from musics_library.menu import Entry,Key,Description

def test_empty_description_raises_exception():
    with pytest.raises(ValidationError):
        Description("")

def test_correct_descriptions():
    correct_values = ['Welcome in Music Library','Welcome_In_Music_Library','Welcome in Music Library!','Welcome: In, Music Library.','Description09']
    for correct in correct_values:
        assert Description(correct)

def test_empty_key_raises_exception():
    with pytest.raises(ValidationError):
        Key("")

def test_key_of_length_11_raises_exception():
    with pytest.raises(ValidationError):
        Key("A"*11)

def test_correct_keys():
    correct_values = ['0','1','2','3','4','5','6','7','8','9','10','A','B','C','A-B','a-b','a_c']
    for correct in correct_values:
        assert Key(correct)
def test_entry_on_selected():
    mocked_on_selected = Mock()
    entry = Entry(Key('1'),Description("Welcome in Music Library"),on_selected=lambda:mocked_on_selected())
    entry.on_selected()
    mocked_on_selected.assert_called_once()

@patch('builtins.print')
def test_entry_is_exit_on_selected(mocked_print):
    entry = Entry(Key('0'), Description('Exit'), on_selected=lambda: print('Bye'), is_exit=True)
    entry.on_selected()
    mocked_print.assert_any_call('Bye')

