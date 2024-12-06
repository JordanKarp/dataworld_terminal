from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from typing import Optional

from classes.email import Email

# from classes.employee import EmployeeRole
from classes.phone_number import Phone
from classes.location import Location
from classes.vehicle import Vehicle
from classes.drivers_license import DriversLicense
from classes.passport import Passport
from classes.age_groups import AgeGroups
from classes.animal import Animal
from classes.bank_account import BankAccount
from classes.social_connect import SocialConnect

from data.person.person_averages import WORKING_AGE, MARRIAGE_AGE


@dataclass
class Person:
    id: str = "P00000"
    gender: str = "Male"
    first_name: str = ""
    middle_name: str = ""
    last_name: str = ""
    nickname: str = ""

    ssn: str = "000-00-0000"
    sexual_orientation: str = "Unknown"
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
    blood_type_allele: str = ""
    mannerisms: str = ""
    positive_traits: str = ""
    neutral_traits: str = ""
    negative_traits: str = ""
    favorites: dict = field(default_factory=dict, repr=True)

    phone_number: Optional[Phone] = None
    email: Optional[Email] = None

    passport: Optional[Passport] = None
    drivers_license: Optional[DriversLicense] = None

    home: Optional[Location] = None
    vehicle: Optional[Vehicle] = None
    bank_account: Optional[BankAccount] = None

    pet: Optional[Animal] = None

    marital_status: Optional[str] = None
    spouse: Optional[Person] = None
    maiden_name: Optional[str] = None
    children: Optional[list[Person]] = None
    siblings: Optional[list[Person]] = None
    parent_a: Optional[Person] = None
    parent_b: Optional[Person] = None

    social_connect: Optional[SocialConnect] = None
    friends: set = field(default_factory=set, init=True, repr=True)

    employer: Optional[str] = None
    role: Optional[str] = None
    salary: Optional[int] = None
    work_days: Optional[list[str]] = None
    work_hours: Optional[list[str]] = None
    patron_of: Optional[list[str]] = None

    def __getitem__(self, item):
        return getattr(self, item, "")

    @property
    def list_of_family(self):
        family = []
        if isinstance(self.parent_a, Person):
            family.append(self.parent_a)
        if isinstance(self.parent_b, Person):
            family.append(self.parent_b)
        if isinstance(self.spouse, Person):
            family.append(self.spouse)
        if isinstance(self.children, list) and self.children != []:
            family.extend(child for child in self.children if isinstance(child, Person))
        if isinstance(self.siblings, list) and self.siblings != []:
            family.extend(
                sibling for sibling in self.siblings if isinstance(sibling, Person)
            )
        return [f for f in family if f is not None]

    @property
    def is_alive(self):
        return not bool(self.date_of_death)

    @property
    def parents(self):
        if self.parent_a and self.parent_b:
            return f"{self.parent_a.name} and {self.parent_b.name}"
        return None

    @property
    def can_work(self):
        return self.age >= WORKING_AGE

    @property
    def can_marry(self):
        return self.age >= MARRIAGE_AGE and self.sexual_orientation != "Asexual"

    @property
    def is_working(self):
        return bool(self.employer)

    @property
    def age_group(self):
        group = AgeGroups.contains(round(self.age))
        return f"{group} (Deceased)" if self.date_of_death else group

    @property
    def full_name(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        else:
            return f"{self.first_name} {self.last_name}"

    @property
    def name(self):
        if self.nickname:
            return f"{self.nickname} {self.last_name}"
        else:
            return f"{self.first_name} {self.last_name}"

    @property
    def last_name_first_initial(self):
        if self.middle_name:
            return f"{self.last_name}, {self.first_name[0]}. {self.middle_name[0]}."
        else:
            return f"{self.last_name}, {self.first_name[0]}."

    @property
    def name_slug(self):
        return "".join(self.name.split(" "))

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
    def desired_gender(self):
        if self.gender in ["Transgender", "Nonbinary"]:
            return self.gender
        if self.gender == "Male":
            return "Male" if self.sexual_orientation == "Homosexual" else "Female"
        if self.gender == "Female":
            return "Female" if self.sexual_orientation == "Homosexual" else "Male"

    @property
    def body_mass_index(self):
        return round((self.weight / (self.height * self.height)) * 703, 1)

    @property
    def format_weight(self):
        return f"{round(self.weight)} lbs"

    @property
    def format_height(self):
        ft, inch = divmod(round(self.height), 12.0)
        return f"{int(ft)}' " + f'{round(inch)}"'

    @property
    def years_lived(self):
        return f"{self.date_of_birth.year} - {self.date_of_death.year if self.date_of_death else ' '}"

    @property
    def blood_type(self):
        _abo, _rh = self.blood_type_allele[:2], self.blood_type_allele[2:]
        abo = _abo if _abo == "AB" else _abo[0]
        rh = "-" if _rh == "dd" else "+"
        return f"{abo}{rh}"

    def __hash__(self):
        # Here we define how we should compute
        # the hash for a given User. In this example
        # we use the hash of the '__email' attribute
        return hash(self.id)

    def __repr__(self):
        return self.id

    def __str__(self):
        return f"{self.full_name} ({self.years_lived})"
