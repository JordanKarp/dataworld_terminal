from faker import Faker
import uuid


from classes.person import Person
from generator_providers.personalDetailsProvider import PersonalDetailsProvider
from generator_providers.locationProvider import LocationProvider
from generator_providers.vehicleProvider import CustomVehicleProvider
from generator_providers.internetProvider import InternetProvider
from generator_providers.documentProvider import DocumentProvider
from generator_providers.animalProvider import AnimalProvider

from data.person.person_averages import WORKING_AGE


class PersonGenerator:
    def __init__(self, seed=None, locations=[]):
        self.gen = Faker()
        if seed:
            Faker.seed(seed)
        self.locations = locations
        self.residences = [
            loc for loc in self.locations if loc.building_type == "Residence"
        ]
        self.gen.add_provider(PersonalDetailsProvider)
        # self.gen.add_provider(LocationProvider)
        self.gen.add_provider(CustomVehicleProvider)
        self.gen.add_provider(InternetProvider)
        self.gen.add_provider(DocumentProvider)
        self.gen.add_provider(AnimalProvider)

    def new_child(self, parent_one, parent_two):
        return self.new(
            last_name=parent_one.last_name,
            generation=parent_one.generation - 1,
            blood_type=self.gen.blood_type_allele(parent_one, parent_two),
            parent_a=parent_one,
            parent_b=parent_two,
            # home=parent_one.home,
        )

    def new(self, **kwargs):
        p = Person(id=f"P{str(uuid.uuid4())[:4]}")

        # EVERYONE #
        ############

        # NAME AND GENDER
        p.gender = kwargs.get("gender", self.gen.gender())
        p.first_name = kwargs.get("first_name", self.gen.first_name_gender(p.gender))
        p.middle_name = kwargs.get("middle_name", self.gen.middle_name_gender(p.gender))
        p.last_name = self.gen.custom_last_name(kwargs.get("last_name", None))
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

        # add cause of death

        p.time_of_birth = kwargs.get("time_of_birth", self.gen.time_of_birth())
        p.ssn = kwargs.get("ssn", self.gen.ssn())
        p.blood_type_allele = kwargs.get("blood_type", self.gen.blood_type_allele())

        # FAMILY
        p.spouse = kwargs.get("spouse", None)
        p.siblings = kwargs.get("siblings", [])
        p.parent_a = kwargs.get("parent_a", None)
        p.parent_b = kwargs.get("parent_b", None)
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
        p.passport = kwargs.get("passport", self.gen.passport(p.date_of_death))
        p.social_connect = kwargs.get("social_connect", self.gen.social_connect(p.name))

        # PERSONALITY
        p.mannerisms = kwargs.get("mannerisms", self.gen.mannerisms())
        p.positive_traits = kwargs.get(
            "positive_traits", self.gen.traits("positive", 3)
        )
        p.neutral_traits = kwargs.get("neutral_traits", self.gen.traits("neutral", 1))
        p.negative_traits = kwargs.get(
            "negative_traits", self.gen.traits("negative", 3)
        )

        p.sexual_orientation = kwargs.get(
            "sexual_orientation", self.gen.sexual_orientation()
        )

        # SIXTEEN
        if p.age < WORKING_AGE:
            return p

        p.patron_of = kwargs.get("patron_of", [])
        p.bank_account = kwargs.get("bank_account", self.gen.bank_account())
        # CAR
        p.drivers_license = kwargs.get(
            "drivers_license", self.gen.drivers_license(p.date_of_death)
        )
        p.vehicle = kwargs.get("vehicle", self.gen.personal_vehicle())

        # EIGHTEEN #
        ############
        if p.age < 18:
            return p

        # PET
        p.pet = kwargs.get("pet", self.gen.new_pet())

        # Marriage
        p.marital_status = kwargs.get("marital_status", "Single")

        # ADULTS #
        ###########
        # LOCATIONS

        p.home = kwargs.get("home", self.get_location())
        return p

    def get_location(self):
        home = self.gen.random_element(self.residences)
        self.residences.remove(home)
        return home
