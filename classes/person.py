from dataclasses import dataclass, field
from datetime import date
from typing import Optional

from classes.email import Email
from classes.phone_number import PhoneNumber
from classes.location import Location
from classes.vehicle import Vehicle
from classes.drivers_license import DriversLicense
from classes.age_groups import AgeGroups


@dataclass
class Person:
    gender: str = "Male"
    first_name: str = ""
    middle_name: str = ""
    last_name: str = ""
    nickname: str = ""
    ssn: str = "000-00-0000"
    sexual_orientation: str = "Heterosexual"
    date_of_birth: date = date(1900, 1, 1)
    time_of_birth: str = ""
    date_of_death: Optional[date] = None
    hair_color: str = "color"
    hair_type: str = "type"
    eye_color: str = "color"
    height: float = 60.0
    weight: float = 100.0
    mannerisms: str = "mannerisms"
    passport_num: str = "A12345678"
    passport_issue_date: date = date(1900, 1, 1)
    passport_exp_date: date = date(1900, 1, 1)
    phone_number: Optional[PhoneNumber] = None
    email: Optional[Email] = None
    home: Optional[Location] = None
    vehicle: Optional[Vehicle] = None
    drivers_license: Optional[DriversLicense] = None
    vehicle: Optional[Vehicle] = None
    siblings: list[str] = field(default_factory=list, repr=True)
    marital_status: str = "Single"
    spouse: Optional[str] = None

    def __getitem__(self, item):
        return getattr(self, item, "")

    @property
    def age(self):
        born = self.date_of_birth
        upperDate = date.today()
        if self.date_of_death:
            upperDate = self.date_of_death
        return (
            upperDate.year
            - born.year
            - ((upperDate.month, upperDate.day) < (born.month, born.day))
        )

    @property
    def age_group(self):
        simple_age = round(self.age)
        for group in AgeGroups:
            if simple_age in group.value:
                return AgeGroups(group.value).name.replace("_", " ").title()

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
        return f"{self.first_name} {self.last_name} - {self.age} - {self.age_group}"
