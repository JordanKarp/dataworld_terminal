from faker import Faker

# from datetime import date

from classes.person import Person
from classes.email import Email
from classes.phone_number import PhoneNumber
from generator_providers.personalDetailsProvider import PersonalDetailsProvider
from generator_providers.locationProvider import LocationProvider
from generator_providers.vehicleProvider import VehicleProvider
from generator_providers.internetProvider import InternetProvider
from generator_utilities.random_tools import blank_or

from data.person.person_averages import MIDDLE_NAME_PERC


class PersonGenerator:
    def __init__(self, seed=None):
        self.gen = Faker()
        if seed:
            Faker.seed(seed)
        self.gen.add_provider(PersonalDetailsProvider)
        self.gen.add_provider(LocationProvider)
        self.gen.add_provider(VehicleProvider)
        self.gen.add_provider(InternetProvider)

    def new(self, **kwargs):
        gender = kwargs.get("gender", self.gen.gender())
        if gender == "Male":
            first_name = kwargs.get("first_name", self.gen.first_name_male())
            middle_name = kwargs.get(
                "middle_name",
                blank_or(self.gen.first_name_male(), MIDDLE_NAME_PERC),
            )
            title = "Mr."
        elif gender == "Female":
            first_name = kwargs.get("first_name", self.gen.first_name_female())
            middle_name = kwargs.get(
                "middle_name",
                blank_or(self.gen.first_name_female(), MIDDLE_NAME_PERC),
            )
            title = "Ms."
        else:
            first_name = kwargs.get("first_name", self.gen.first_name_nonbinary())
            middle_name = kwargs.get(
                "middle_name",
                blank_or(self.gen.first_name_nonbinary(), MIDDLE_NAME_PERC),
            )
            title = "Mx."
        last_name = kwargs.get("last_name", self.gen.last_name())
        height = kwargs.get("height", self.gen.height())
        weight = kwargs.get("weight", self.gen.weight())
        hair_color = kwargs.get("hair_color", self.gen.hair_color())
        hair_type = kwargs.get("hair_type", self.gen.hair_type())
        eye_color = kwargs.get("eye_color", self.gen.eye_color())
        mannerisms = kwargs.get("mannerisms", self.gen.mannerisms())
        home = kwargs.get("home", self.gen.home())

        # date_of_birth = kwargs.get("date_of_birth", self.gen.date_of_birth())

        date_of_birth = self.gen.birthday(kwargs.get("date_of_birth", None))

        ssn = kwargs.get("ssn", self.gen.ssn())

        email = Email(
            kwargs.get("email", self.gen.email(first_name, last_name, date_of_birth))
        )
        phone_number = PhoneNumber(kwargs.get("phone_number", self.gen.phone_number()))

        siblings = kwargs.get("siblings", [])
        vehicle = kwargs.get("vehicle", self.gen.personal_vehicle())
        sexual_orientation = kwargs.get(
            "sexual_orientation", self.gen.sexual_orientation()
        )

        return Person(
            gender=gender,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            title=title,
            height=height,
            weight=weight,
            hair_color=hair_color,
            hair_type=hair_type,
            eye_color=eye_color,
            mannerisms=mannerisms,
            date_of_birth=date_of_birth,
            ssn=ssn,
            email=email,
            phone_number=phone_number,
            home=home,
            vehicle=vehicle,
            sexual_orientation=sexual_orientation,
            siblings=siblings,
        )
