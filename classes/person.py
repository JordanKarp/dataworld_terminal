from dataclasses import dataclass
from datetime import date

from classes.email import Email
from classes.phone_number import PhoneNumber
from classes.location import Location
from classes.vehicle import Vehicle


@dataclass
class Person:
    first_name: str = "defFirstName"
    middle_name: str = ""
    last_name: str = ""
    nickname: str = ""
    title: str = "defTitle"
    gender: str = "Male"
    ssn: str = "000-00-0000"
    date_of_birth: date = "None"
    date_of_death: date = None
    hair_color: str = "color"
    hair_type: str = "type"
    eye_color: str = "color"
    height: str = "height"
    weight: str = "weight"
    mannerisms: str = "mannerisms"
    phone_number: PhoneNumber = None
    email: Email = None
    home: Location = None
    vehicle: Vehicle = None

    @property
    def age(self):
        return "TBD"

    @property
    def gender_abbr(self):
        return self.gender[0]

    @property
    def format_weight(self):
        return f"{self.weight} lbs"

    @property
    def format_height(self):
        ft, inch = divmod(self.height, 12)
        return f"{int(ft)}' " + f'{round(inch)}"'
