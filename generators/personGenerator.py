from faker import Faker

from classes.person import Person
from generator_providers.personalDetailsProvider import PersonalDetailsProvider
from generator_providers.locationProvider import LocationProvider
from generator_providers.vehicleProvider import CustomVehicleProvider
from generator_providers.internetProvider import InternetProvider
from generator_providers.documentProvider import DocumentProvider

from data.person.person_averages import (
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
        self.gen.add_provider(DocumentProvider)

    # def new_sibling(self, original_person):
    #     return self.new(
    #         last_name=original_person.last_name,
    #         date_of_birth=original_person.date_of_birth,
    #     )

    def new_child(self, parent_one, parent_two):
        return self.new(
            last_name=parent_one.last_name,
            generation=parent_one.generation - 1,
            home=parent_one.home,
        )

    def new_spouse(self, original_person):
        gender_map = {
            "Homosexual": original_person.gender,
            "Bisexual": self.gen.random_element(["Male", "Female"]),
            "Heterosexual": "Female" if original_person.gender == "Male" else "Male",
        }
        new_gender = gender_map.get(original_person.sexual_orientation, "Male")
        last_name = (
            original_person.last_name
            if self.gen.percent_check(TAKE_NAME_PERCENT)
            else None
        )
        return self.new(
            spouse=original_person,
            last_name=last_name,
            gender=new_gender,
            sexual_orientation=original_person.sexual_orientation,
            marital_status="Married",
            generation=original_person.generation,
            home=original_person.home,
        )

    def new(self, **kwargs):
        self.counter += 1
        p = Person(id=f"P{self.counter:04d}")

        # EVERYONE #
        ############

        # NAME AND GENDER
        p.gender = kwargs.get("gender", self.gen.gender())
        p.first_name = kwargs.get("first_name", self.gen.first_name_gender(p.gender))
        p.middle_name = kwargs.get("middle_name", self.gen.middle_name_gender(p.gender))
        p.last_name = kwargs.get("last_name", self.gen.last_name())
        p.nickname = kwargs.get(
            "nickname", self.gen.nickname(p.first_name, p.middle_name)
        )

        # INFO
        p.generation = kwargs.get("generation", 0)
        p.date_of_birth = kwargs.get(
            "date_of_birth", self.gen.date_of_birth_generation(p.generation)
        )
        p.date_of_death = kwargs.get(
            "date_of_death",
            self.gen.date_of_death(p.date_of_birth, p.generation),
        )
        p.age = kwargs.get("age", self.gen.age(p.date_of_birth, p.date_of_death))
        p.time_of_birth = kwargs.get("time_of_birth", self.gen.time_of_birth())
        p.ssn = kwargs.get("ssn", self.gen.ssn())

        # FAMILY
        p.siblings = kwargs.get("siblings", [])
        p.children = kwargs.get("children", [])

        # BODY
        p.height = kwargs.get("height", self.gen.height(p.gender))
        p.weight = kwargs.get("weight", self.gen.weight(p.gender))
        p.hair_color = kwargs.get("hair_color", self.gen.hair_color())
        p.hair_type = kwargs.get("hair_type", self.gen.hair_type())
        p.eye_color = kwargs.get("eye_color", self.gen.eye_color())

        # CHILD #
        #########
        if p.age < 13:
            return p

        # TEEN #
        ########
        p.phone_number = kwargs.get("phone_number", self.gen.phone_number())
        p.email = kwargs.get(
            "email",
            self.gen.email(p.first_name, p.last_name, p.date_of_birth),
        )
        p.passport = kwargs.get("passport", self.gen.passport())

        # PERSONALITY
        p.mannerisms = kwargs.get("mannerisms", self.gen.mannerisms())
        p.sexual_orientation = kwargs.get(
            "sexual_orientation", self.gen.sexual_orientation()
        )

        # EIGHTEEN #
        ############
        if p.age < 18:
            return p

        # CAR
        p.vehicle = kwargs.get("vehicle", self.gen.personal_vehicle())
        p.drivers_license = kwargs.get("drivers_license", self.gen.drivers_license())

        # Marriage
        p.marital_status = kwargs.get("marital_status", "Single")
        p.spouse = kwargs.get("spouse", None)

        # ADULTS #
        ###########
        # LOCATIONS
        p.home = kwargs.get("home", self.gen.home())

        return p
