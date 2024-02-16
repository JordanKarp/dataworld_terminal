from dataclasses import dataclass

from classes.person import Person


@dataclass
class Employee:
    person: Person
    id: str
    team: str
    role: str
    # id
    # hours: str

    def __getitem__(self, item):
        return getattr(self, item, "")
