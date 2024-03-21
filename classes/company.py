from dataclasses import dataclass, field
from typing import Optional
from random import choice

from classes.location import Location
from classes.employee import EmployeeRole
from classes.person import Person
from classes.industries import Industries

# from classes.person import Person


@dataclass
class Company:
    id: str = "C00000"
    company_name: str = ""
    website: str = ""
    industry: Optional[Industries] = None
    sub_industry: str = ""
    employee_structure: Optional[list[EmployeeRole]] = None
    # employee_structure: list[EmployeeRole] = field(
    #     default_factory=list, repr=True, init=True
    # )
    main_phone: list[str] = field(default_factory=list, repr=True)
    founded: int = 1900
    social_media: list[str] = field(default_factory=list, repr=True)
    client_scope: str = "International"
    clients: list[Person] = field(default_factory=list, repr=True)
    hq: Optional[Location] = None
    locations: list[Location] = field(default_factory=list, repr=True)
    market_share: Optional[float] = 0.25
    # data: list[str] = field(default_factory=list, repr=True)

    @property
    def abbreviation(self):
        return "".join([l for l in self.company_name if l.isupper()])
        # return "".join([n[0] for n in self.company_name.split(" ")])

    @property
    def num_employees_hired(self):
        return sum(1 if x.is_filled else 0 for x in self.employee_structure)

    @property
    def num_employees_needed(self):
        return len(self.employee_structure)

    @property
    def room_to_hire(self):
        return self.num_employees_needed - self.num_employees_hired > 0

    @property
    def employee_nums(self):
        return f"{self.num_employees_hired} / {self.num_employees_needed}"

    @property
    def num_clients(self):
        return len(self.clients)

    def add_employee(self, person):
        available_roles = [r for r in self.employee_structure if not r.is_filled]
        if not available_roles:
            return None  # Handle the case where there are no available roles
        role = choice(available_roles)
        role.person = person
        return role

    def add_client(self, person):
        # add more client info like persons id number, etc here.
        person.patron_of = getattr(person, "patron_of", [])
        person.patron_of.append(self)

        self.clients.append(person)

    def __repr__(self):
        return f"{self.company_name} ({self.founded}) - {self.industry}: {self.sub_industry}"

    def __getitem__(self, item):
        return getattr(self, item, "")

    def __iter__(self):
        return iter(self.__dict__.values())
