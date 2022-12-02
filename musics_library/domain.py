from password_validator import PasswordValidator
from typeguard import typechecked
from dataclasses import dataclass
from valid8 import validate
from validation.regex import pattern

@typechecked
@dataclass(frozen=True,order=True)
class Name:
    value: str
    def __post_init__(self):
        validate('value', self.value, min_len=1, max_len=50, custom=pattern(r'[A-Za-z0-9- ,!@]*'))
    def __str__(self):
        return self.value

@typechecked
@dataclass(frozen=True,order=True)
class Artist:
    value:str

    def __post_init__(self):
        validate('value', self.value, min_len=1, max_len=50, custom=pattern(r'[A-Za-z0-9- ,!@]*'))

    def __str__(self):
        return self.value

@typechecked
@dataclass(frozen=True,order=True)
class RecordCompany:
    value:str

    def __post_init__(self):
        validate('value', self.value, min_len=1, max_len=50, custom=pattern(r'[A-Za-z0-9- ,!@#]*'))

    def __str__(self):
        return self.value

@typechecked
@dataclass(frozen=True,order=True)
class Genre:
    value: str

    def __post_init__(self):
        validate('value', self.value, min_len=1, max_len=25, custom=pattern(r'^[A-Z][A-Za-z ]*'))

    def __str__(self):
        return self.value

@typechecked
@dataclass(frozen=True,order=True)
class EANCode:
    pass



#PIGLIARE DA ALVIANO
@typechecked
@dataclass(frozen=True,order=True)
class Price:
    pass

#TODO Published-by, Created-at, Updated-At

@typechecked
@dataclass(frozen=True,order=True)
class Email:
    value: str

    def __post_init__(self):
        validate('value', self.value, min_len=1, max_len=150, custom=pattern(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'))

    def __str__(self):
        return self.value

#TODO created_at - updated_at CREIAMO GIORNI MESI ANNO come value objects oppure usiamo datetime()
@typechecked
@dataclass(frozen=True,order=True)
class Username:
    value:str

    def __post_init__(self):
        validate('value', self.value, min_len=1, max_len=150, custom=pattern(r'[A-Za-z0-9]*'))

    def __str__(self):
        return self.value


@typechecked
@dataclass(frozen=True,order=True)
class Password:
    value:str

    def __post_init__(self):
        schema = PasswordValidator()
        schema\
            .min(8)\
            .max(128)\
            .has().no().spaces()\
            .has().uppercase()\
            .has().lowercase()\
            .has(r'[\@|\!|\.|\-]*')
        validation = schema.validate(self.value)
        if(not validation):
            raise ValueError("Password isn't valid")


#TODO User