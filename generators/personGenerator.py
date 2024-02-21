from faker import Faker
from dateutil.relativedelta import relativedelta

from classes.person import Person
from generator_providers.personalDetailsProvider import PersonalDetailsProvider
from generator_providers.locationProvider import LocationProvider
from generator_providers.vehicleProvider import CustomVehicleProvider
from generator_providers.internetProvider import InternetProvider
from generator_providers.choicesProvider import ChoicesProvider

from data.person.person_averages import (
    YEARS_TIL_PASSPORT_EXP,
    TAKE_NAME_PERCENT,
)


class PersonGenerator:
    def __init__(self, seed=None):
        self.gen = Faker()
        if seed:
            Faker.seed(seed)
        self.counter = 0
        self.gen.add_provider(PersonalDetailsProvider)
        self.gen.add_provider(LocationProvider)
        self.gen.add_provider(CustomVehicleProvider)
        self.gen.add_provider(InternetProvider)
        self.gen.add_provider(ChoicesProvider)

    def new_sibling(self, original_person):
        return self.new(
            last_name=original_person.last_name,
            date_of_birth=original_person.date_of_birth,
        )

    def new_spouse(self, original_person):
        if original_person.sexual_orientation == "Homosexual":
            new_gender = original_person.gender
        elif original_person.sexual_orientation == "Bisexual":
            new_gender = self.gen.random_element(["Male", "Female"])
        else:
            new_gender = "Female" if original_person.gender == "Male" else "Male"

        if self.gen.boolean(TAKE_NAME_PERCENT * 100):
            # if self.gen.pybool():
            return self.new(
                spouse=original_person,
                last_name=original_person.last_name,
                gender=new_gender,
                marital_status=original_person.marital_status,
                date_of_birth=original_person.date_of_birth,
                home=original_person.home,
            )
        else:
            return self.new(
                spouse=original_person,
                gender=new_gender,
                marital_status=original_person.marital_status,
                date_of_birth=original_person.date_of_birth,
                home=original_person.home,
            )

    def new(self, **kwargs):
        self.counter += 1
        person = Person(id=f"P{self.counter:05d}")

        # NAME AND GENDER
        person.gender = kwargs.get("gender", self.gen.gender())
        person.first_name = kwargs.get(
            "first_name", self.gen.first_name_gender(person.gender)
        )
        person.middle_name = kwargs.get(
            "middle_name", self.gen.middle_name_gender(person.gender)
        )
        person.last_name = kwargs.get("last_name", self.gen.last_name())
        person.nickname = kwargs.get(
            "nickname", self.gen.nickname(person.first_name, person.middle_name)
        )

        # INFO
        person.date_of_birth = self.gen.birthday(kwargs.get("date_of_birth", None))
        person.time_of_birth = kwargs.get("time_of_birth", self.gen.time_of_birth())
        person.date_of_death = kwargs.get(
            "date_of_death", self.gen.date_of_death(person.age)
        )

        # BODY
        person.height = kwargs.get("height", self.gen.height(person.gender))
        person.weight = kwargs.get("weight", self.gen.weight(person.gender))
        person.hair_color = kwargs.get("hair_color", self.gen.hair_color())
        person.hair_type = kwargs.get("hair_type", self.gen.hair_type())
        person.eye_color = kwargs.get("eye_color", self.gen.eye_color())

        # PERSONALITY
        person.mannerisms = kwargs.get("mannerisms", self.gen.mannerisms())

        # LOCATIONS
        person.home = kwargs.get("home", self.gen.home())

        #
        person.ssn = kwargs.get("ssn", self.gen.ssn())
        person.email = kwargs.get(
            "email",
            self.gen.email(person.first_name, person.last_name, person.date_of_birth),
        )
        person.phone_number = kwargs.get("phone_number", self.gen.phone_number())
        person.sexual_orientation = kwargs.get(
            "sexual_orientation", self.gen.sexual_orientation()
        )
        person.marital_status = kwargs.get("martial_status", "Single")

        person.passport_num = kwargs.get("passport_num", self.gen.passport_num())
        person.passport_issue_date = kwargs.get(
            "passport_issue_date", self.gen.passport_issue_date()
        )
        person.passport_exp_date = kwargs.get(
            "passport_exp_date",
            person.passport_issue_date + relativedelta(years=YEARS_TIL_PASSPORT_EXP),
        )

        # FAMILY
        person.siblings = kwargs.get("siblings", [])
        person.spouse = kwargs.get("spouse", None)

        # CAR
        person.vehicle = kwargs.get("vehicle", self.gen.personal_vehicle())
        person.drivers_license = kwargs.get(
            "drivers_license", self.gen.drivers_license()
        )

        return person
