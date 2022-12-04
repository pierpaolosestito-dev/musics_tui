import json
from datetime import datetime

from password_validator import PasswordValidator
from typeguard import typechecked
from typing import Any, List
from dataclasses import dataclass, InitVar, field
from valid8 import validate, ValidationError


from validation.regex import pattern
import re
from stdnum.util import clean, isdigits

@typechecked
@dataclass(frozen=True,order=True)
class ID:
    value: int

    def __post_init__(self):
        validate('value',self.value,min_value=0)

    def __str__(self):
        return self.value

@typechecked
@dataclass(frozen=True, order=True)
class Name:
    value: str

    def __post_init__(self):
        validate('value', self.value, min_len=1, max_len=50, custom=pattern(r'[A-Za-z0-9- ,!@]*'))

    def __str__(self):
        return self.value


@typechecked
@dataclass(frozen=True, order=True)
class Artist:
    value: str

    def __post_init__(self):
        validate('value', self.value, min_len=1, max_len=50, custom=pattern(r'[A-Za-z0-9- ,!@]*'))

    def __str__(self):
        return self.value


@typechecked
@dataclass(frozen=True, order=True)
class RecordCompany:
    value: str

    def __post_init__(self):
        validate('value', self.value, min_len=1, max_len=50, custom=pattern(r'[A-Za-z0-9- ,!@#]*'))

    def __str__(self):
        return self.value


@typechecked
@dataclass(frozen=True, order=True)
class Genre:
    value: str

    def __post_init__(self):
        validate('value', self.value, min_len=1, max_len=25, custom=pattern(r'^[A-Z][A-Za-z ]*'))

    def __str__(self):
        return self.value


@typechecked
@dataclass(frozen=True, order=True)
class EANCode:
    value: str

    def __post_init__(self):
        self.__validate_ean(self.value)

    def __compact(self, number):
        return clean(number, ' -').strip()

    def __calc_check_digit(self, number):
        return str((10 - sum((3, 1)[i % 2] * int(n)
                             for i, n in enumerate(reversed(number)))) % 10)

    def __validate(self, number):
        number = self.__compact(number)
        if not isdigits(number):
            raise ValidationError("EANCode is structured with numbers.")
        if len(number) not in (14, 13, 12, 8):
            raise ValidationError("EANCode length isn't correct.")
        if self.__calc_check_digit(number[:-1]) != number[-1]:
            raise ValidationError("Checksum fails.")
        return number

    def __validate_ean(self, number):
        try:
            return bool(self.__validate(number))
        except ValidationError:
            return False

    def __str__(self):
        return self.value


@typechecked
@dataclass(frozen=True, order=True)
class Discount:
    value_in_thousands: int

    def __post_init__(self):
        validate('value_in_thousands', self.value_in_thousands, min_value=0, max_value=1000)

    def __str__(self):
        return f'{self.value_in_thousands // 10}.{self.value_in_thousands % 10}%'

    def apply(self, value: int):
        return value * (1000 - self.value_in_thousands) // 1000


@typechecked
@dataclass(frozen=True, order=True)
class Price:
    value_in_cents: int
    create_key: InitVar[Any] = field(default=None)
    __create_key = object()
    __max_value = 100000000000 - 1
    __parse_pattern = re.compile(r'(?P<euro>\d{0,11})(?:\.(?P<cents>\d{2}))?')

    def __post_init__(self, create_key):
        validate('create_key', create_key, equals=self.__create_key)
        validate('value_in_cents', self.value_in_cents, min_value=0, max_value=self.__max_value)

    def __str__(self):
        return f'{self.value_in_cents // 100}.{self.value_in_cents % 100:02}'

    @staticmethod
    def create(euro: int, cents: int = 0) -> 'Price':
        validate('euro', euro, min_value=0, max_value=Price.__max_value // 100)
        validate('cents', cents, min_value=0, max_value=99)
        return Price(euro * 100 + cents, Price.__create_key)

    @staticmethod
    def parse(value: str) -> 'Price':
        n = Price.__parse_pattern.fullmatch(value)
        validate('value', n)
        euro = n.group('euro')
        cents = n.group('cents') if n.group('cents') else 0
        return Price.create(int(euro), int(cents))

    @property
    def cents(self) -> int:
        return self.value_in_cents % 100

    @property
    def euro(self) -> int:
        return self.value_in_cents // 100

    def add(self, other: 'Price') -> 'Price':
        return Price(self.value_in_cents + other.value_in_cents, self.__create_key)

    def apply_discount(self, discount: Discount) -> 'Price':
        return Price(discount.apply(self.value_in_cents), self.__create_key)


# TODO Published-by, Created-at, Updated-At

@typechecked
@dataclass(frozen=True, order=True)
class Email:
    value: str

    def __post_init__(self):
        validate('value', self.value, min_len=1, max_len=150,
                 custom=pattern(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'))

    def __str__(self):
        return self.value


# TODO created_at - updated_at CREIAMO GIORNI MESI ANNO come value objects oppure usiamo datetime()
@typechecked
@dataclass(frozen=True, order=True)
class Username:
    value: str

    def __post_init__(self):
        validate('value', self.value, min_len=1, max_len=150, custom=pattern(r'[A-Za-z0-9-]*'))

    def __str__(self):
        return self.value


@typechecked
@dataclass(frozen=True, order=True)
class Password:
    value: str

    def __post_init__(self):
        schema = PasswordValidator()
        schema \
            .min(8) \
            .max(128) \
            .has().no().spaces() \
            .has().lowercase() \
            .has(r'[\@|\!|\.|\-]*')
        validation = schema.validate(self.value)
        if (not validation):
            raise ValueError("Password isn't valid")


@typechecked
@dataclass(frozen=True)
class Music:
    id: ID
    name: Name
    artist: Artist
    record_company: RecordCompany
    genre: Genre
    ean_code: EANCode
    published_by: Username
    price: Price
    created_at: datetime
    updated_at: datetime

    @property
    def music_id(self):
        return self.id


@typechecked
@dataclass(frozen=True)
class MusicLibrary:
    #Ho un problema, se importo MusicsService qua dentro mi da un problema di\
    #Circular Import perché dentro MusicsService usiamo alcune classi del domain.
    def musics(self):
        pass

    def music(self):
        pass

    def add_music(self,music:Music):
        pass

    def update_music(self,music:Music):
        pass


    def remove_music(self,id:ID):
        pass

    def musics_by_artist(self,artist:Artist):
        pass

    def musics_by_published_by(self,published_by:Username):
        pass

    def musics_by_cd_name(self,cd_name:Name):
        pass

    def sort_musics_by_price(self):
        pass



