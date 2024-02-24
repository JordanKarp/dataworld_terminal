from dataclasses import dataclass, field
from typing import Optional
from random import choice

# from classes.location import Location
from classes.employee import EmployeeRole
from classes.industries import Industries

# from classes.person import Person


@dataclass
class Company:
    id: str = "C00000"
    name: str = ""
    website: str = ""
    industry: Optional[Industries] = None
    sub_industry: str = ""
    employee_structure: list[EmployeeRole] = field(default_factory=list, repr=True)
    main_phone: list[str] = field(default_factory=list, repr=True)
    founded: int = 1900
    # locations: list[Location] = field(default_factory=list, repr=True)
    social_media: list[str] = field(default_factory=list, repr=True)
    # data: list[str] = field(default_factory=list, repr=True)
    # counter: int = field(default=1, repr=False)

    @property
    def abbreviation(self):
        return "".join([n[0] for n in self.name.split(" ")])

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

    def add_employee(self, person):
        available_roles = [r for r in self.employee_structure if not r.is_filled]
        role = choice(available_roles)
        role.person = person
        return role

    def __repr__(self):
        return f"{self.name} ({self.founded}) - {self.industry}: {self.sub_industry}"

    def __getitem__(self, item):
        return getattr(self, item, "")

    def __iter__(self):
        return iter([v for k, v in self.__dict__.items() if not k.startswith("__")])
