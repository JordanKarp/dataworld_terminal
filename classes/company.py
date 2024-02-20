from dataclasses import dataclass, field

# from classes.location import Location
from classes.employee import EmployeeDemand
from classes.industries import Industries

# from classes.person import Person


@dataclass
class Company:
    # id
    name: str
    website: str
    industry: Industries
    sub_industry: str
    employee_structure: list[EmployeeDemand] = field(default_factory=list, repr=True)
    main_phone: list[str] = field(default_factory=list, repr=True)
    # locations: list[Location] = field(default_factory=list, repr=True)
    social_media: list[str] = field(default_factory=list, repr=True)
    # staff: list[Employee] = field(default_factory=list, repr=True)
    # data: list[str] = field(default_factory=list, repr=True)
    # counter: int = field(default=1, repr=False)

    # def create_id(self) -> str:
    #     """Creates an id like ac00001 for the first employee at AcmeCo"""
    #     abbrev = self.name[:2].upper()
    #     num = str(self.counter).zfill(5)
    #     self.counter += 1
    #     return "".join((abbrev, num))

    def __repr__(self):
        return f"{self.name} ({self.industry}:{self.sub_industry}) - {self.website}"

    def __getitem__(self, item):
        return getattr(self, item, "")

    # def add_employee(self, person: Person, role: str, team: str):
    #     employee = Employee(
    #         company=self, person=person, role=role, team=team, id=self.create_id()
    #     )
    #     self.staff.append(employee)
