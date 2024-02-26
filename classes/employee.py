from dataclasses import dataclass
from typing import Optional

from classes.person import Person


@dataclass
class EmployeeRole:
    role_name: str = "Employee"
    team_name: str = "General"
    person: Optional[Person] = None

    @property
    def is_filled(self):
        return bool(self.person)

    def __getitem__(self, item):
        return getattr(self, item, "")

    def __str__(self):
        return f"{self.role_name}: {self.team_name}"

    def __repr__(self):
        if self.person:
            return f"{self.role_name}:{self.person.id}"
        else:
            return f"{self.role_name}"


# @dataclass
# class EmployeeDemand:
#     role: EmployeeRole
#     needed: int = 1

#     def __getitem__(self, item):
#         return getattr(self, item, "")

#     def __repr__(self):
#         return f"{self.needed} {self.role}"

#     def __str__(self):
#         return f"{self.needed} {self.role}"


# @dataclass
# class Employee:
#     person: Person
#     id: str
#     team: str
#     role: str
#     # id
#     # hours: str

#     def __getitem__(self, item):
#         return getattr(self, item, "")
