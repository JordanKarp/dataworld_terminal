from dataclasses import dataclass, field
from typing import Optional
from random import choice

from classes.location import Location
from classes.employee import EmployeeRole, WorkLocation
from classes.person import Person

# from classes.industries import Industries
from classes.bank_account import BankAccount

# from classes.person import Person


@dataclass
class Company:
    id: str = "C00000"
    name: str = ""
    slogan: str = ""
    opener: str = ""
    industry: str = ""
    products: Optional[list[str]] = None
    # sub_industry: str = ""
    employee_structure: Optional[list[EmployeeRole]] = None
    main_phone: list[str] = field(default_factory=list, repr=True)
    email: Optional[str] = None
    founded: int = 1900
    social_media: list[str] = field(default_factory=list, repr=True)
    client_scope: str = "International"
    clients: list[Person] = field(default_factory=list, repr=True)
    # hq: Optional[Location] = None
    locations: Optional[list[WorkLocation]] = None
    bank_account: Optional[BankAccount] = None
    # locations: list[Location] = field(default_factory=list, repr=True)
    # physical_locations: list[WorkLocation] = field(default_factory=list, repr=True)
    market_share: Optional[float] = 0.25
    website_font_color: str = "#000000"
    # data: list[str] = field(default_factory=list, repr=True)

    @property
    def abbreviation(self):
        return "".join([letter for letter in self.name if letter.isupper()])

    # @property
    # def num_employees_hired(self):
    #     return (
    #         sum(1 if x.is_filled else 0 for x in self.employee_structure)
    #         if self.employee_structure
    #         else 0
    #     )
    @property
    def num_employees_hired(self):
        if not self.locations:
            return 0
        return sum(emp.is_filled for loc in self.locations for emp in loc.employees)

    @property
    def num_employees_needed(self):
        if not self.locations:
            return 0
        return sum(1 for loc in self.locations for emp in loc.employees)

    @property
    def room_to_hire(self):
        return self.num_employees_needed - self.num_employees_hired > 0

    @property
    def employee_nums(self):
        return f"{self.num_employees_hired} / {self.num_employees_needed}"

    @property
    def num_clients(self):
        return len(self.clients)

    @property
    def slug(self):
        return self.name.replace(" ", "").lower()

    # @property
    # def website_url(self):
    #     return f"www.{self.slug}.com"

    @property
    def homepage_html(self):
        s = (
            "<body>"
            f"<font color='{self.website_font_color}'>"
            f"<font size='6'><b>{self.name}</b></font><br>"
            "<br>"
            f"{self.slogan}<br>"
            f"Leaders in {self.industry}<br>"
            f"{self.opener}"
            "<br>"
            f" - <a href={self.slug}~about>About Us</a><br>"
            f" - <a href={self.slug}~contact>Contact</a><br>"
            "</font></body>"
        )
        return s

    @property
    def about_html(self):
        s = (
            "<body>"
            f"<font color='{self.website_font_color}'>"
            f"<font size='6'><b>{self.name}: About Us</b></font><br>"
            "<br>"
            f"{self.opener}<br>"
            f"<a href={self.slug}>Homepage</a><br>"
        )
        if self.employee_structure:
            s += "<u>Employees:</u><br>"
            for employee in self.employee_structure:
                if employee.person:
                    s += f" - <b>{employee.role_name}</b>: {employee.person.name}<br>"

        s += "</font></body>"
        return s

    @property
    def contact_html(self):
        s = (
            "<body>"
            f"<font color='{self.website_font_color}'>"
            f"<font size='6'><b>{self.name}: Contact Us</b></font><br>"
            "<br>"
            f"{self.slogan}<br>"
            "<br>"
            f"<a href={self.slug}>Homepage</a><br>"
        )
        if self.main_phone:
            s += f"Phone: {self.main_phone}<br>"
        if self.email:
            s += f"Email: {self.email}<br>"
        # if self.hq:
        #     s += f"Headquarters: {self.hq.address}<br>"
        if self.locations:
            # s += f"{(str(l.location.address) for l in self.locations)}<br>"
            for loc in self.locations:
                s += loc.location.address
        s += "</font></body>"
        return s

    @property
    def zip_codes(self):
        if not self.locations:
            return None
        return [loc.location.zipcode for loc in self.locations]

    @property
    def states(self):
        if not self.locations:
            return None
        return [loc.location.state for loc in self.locations]

    def add_employee(self, person):
        if not self.locations:
            return None

        available_roles = [
            emp for loc in self.locations for emp in loc.employees if not emp.is_filled
        ]

        if not available_roles:
            return None  # Handle the case where there are no available roles

        role = choice(available_roles)
        role.person = person
        person.salary = role.salary
        person.role = role
        person.employer = self
        person.work_days = role.work_days
        person.work_hours = role.work_hours
        # person.work_days = list(range(5))
        # person.work_hours = list(range(8, 18))
        # return role

    def add_client(self, person):
        # TODO add more client info like persons id number, etc here.
        person.patron_of = getattr(person, "patron_of", [])
        person.patron_of.append(self)

        self.clients.append(person)

    def __repr__(self):
        return f"{self.name} ({self.founded}) - {self.industry}"

    def __getitem__(self, item):
        return getattr(self, item, "")

    # def __iter__(self):
    #     return iter(self.__dict__.values())
