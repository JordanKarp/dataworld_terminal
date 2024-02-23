from dataclasses import dataclass, field
from datetime import date
from typing import Optional

from classes.email import Email
from classes.phone_number import PhoneNumber
from classes.location import Location
from classes.vehicle import Vehicle
from classes.drivers_license import DriversLicense
from classes.passport import Passport
from classes.age_groups import AgeGroups


@dataclass
class Person:
    id: str = "P00000"
    gender: str = "Male"
    first_name: str = ""
    middle_name: str = ""
    last_name: str = ""
    nickname: str = ""
    ssn: str = "000-00-0000"
    sexual_orientation: str = "Heterosexual"
    age: int = 0
    generation: int = 0
    date_of_birth: date = date(1900, 1, 1)
    time_of_birth: str = ""
    date_of_death: Optional[date] = None
    hair_color: str = ""
    hair_type: str = ""
    eye_color: str = ""
    height: float = 60.0
    weight: float = 100.0
    mannerisms: str = ""
    passport: Optional[Passport] = None
    phone_number: Optional[PhoneNumber] = None
    email: Optional[Email] = None
    home: Optional[Location] = None
    vehicle: Optional[Vehicle] = None
    drivers_license: Optional[DriversLicense] = None
    siblings: list[str] = field(default_factory=list, repr=True)
    marital_status: str = "Single"
    spouse: Optional[str] = None

    # _age_cache: Optional[int] = field(default=None, init=False, repr=False)

    def __getitem__(self, item):
        return getattr(self, item, "")

    # @property
    # def age(self):
    #     if self._age_cache is None:
    #         born = self.date_of_birth
    #         upperDate = self.date_of_death or date.today()
    #         self._age_cache = (
    #             upperDate.year
    #             - born.year
    #             - ((upperDate.month, upperDate.day) < (born.month, born.day))
    #         )
    #     return self._age_cache

    @property
    def age_group(self):
        return AgeGroups.contains(round(self.age))

    @property
    def full_name(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        else:
            return f"{self.first_name} {self.last_name}"

    @property
    def title(self):
        if self.gender == "Female":
            return "Mrs." if self.marital_status == "Married" else "Ms."
        elif self.gender == "Male":
            return "Mr."
        else:
            return "Mx."

    @property
    def gender_abbr(self):
        return self.gender[0]

    @property
    def format_weight(self):
        return f"{round(self.weight)} lbs"

    @property
    def format_height(self):
        ft, inch = divmod(round(self.height), 12.0)
        return f"{int(ft)}' " + f'{round(inch)}"'

    @property
    def vehicle_details(self):
        if self.vehicle:
            return self.vehicle.vehicle_fields

    def __repr__(self):
        return f"{self.first_name}, {self.date_of_birth} "

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.age} - {self.date_of_birth}"
