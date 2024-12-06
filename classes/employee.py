from dataclasses import dataclass, field
from typing import Optional

from classes.person import Person
from classes.location import Location


WEEKDAYS = [0, 1, 2, 3, 4]
NINE_TO_FIVE = [9, 10, 11, 12, 13, 14, 15, 16, 17]


@dataclass
class EmployeeRole:
    role_name: str = "Employee"
    team_name: str = "General"
    salary: int = 2000
    person: Optional[Person] = None
    work_days: list[int] = field(default_factory=lambda: WEEKDAYS, repr=True)
    work_hours: list[int] = field(default_factory=lambda: NINE_TO_FIVE, repr=True)

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


@dataclass
class WorkLocation:
    location: Location
    employees: list[EmployeeRole]
    location_name: str = "Store"
