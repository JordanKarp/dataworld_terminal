from faker import Faker
from dateutil.relativedelta import relativedelta

from classes.person import Person
from classes.email import Email
from classes.phone_number import PhoneNumber
from generator_providers.personalDetailsProvider import PersonalDetailsProvider
from generator_providers.locationProvider import LocationProvider
from generator_providers.vehicleProvider import VehicleProvider
from generator_providers.internetProvider import InternetProvider
from generator_providers.choicesProvider import ChoicesProvider
from generator_utilities.random_tools import blank_or

from data.person.person_averages import (
    MIDDLE_NAME_PERC,
    YEARS_TIL_DL_EXP,
    YEARS_TIL_PASSPORT_EXP,
    TAKE_NAME_PERCENT,
)


class PersonGenerator:
    def __init__(self, seed=None):
        self.gen = Faker()
        if seed:
            Faker.seed(seed)
        self.gen.add_provider(PersonalDetailsProvider)
        self.gen.add_provider(LocationProvider)
        self.gen.add_provider(VehicleProvider)
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
        # NAME AND GENDER
        gender = kwargs.get("gender", self.gen.gender())
        if gender == "Male":
            first_name = kwargs.get("first_name", self.gen.first_name_male())
            middle_name = kwargs.get(
                "middle_name",
                blank_or(self.gen.first_name_male(), MIDDLE_NAME_PERC),
            )
            nickname = kwargs.get(
                "nickname", self.gen.nickname(first_name, middle_name)
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
        nickname = kwargs.get("nickname", self.gen.nickname(first_name, middle_name))

        # INFO
        date_of_birth = self.gen.birthday(kwargs.get("date_of_birth", None))
        time_of_birth = kwargs.get("time_of_birth", self.gen.time_of_birth())

        # BODY
        height = kwargs.get("height", self.gen.height(gender))
        weight = kwargs.get("weight", self.gen.weight(gender))
        hair_color = kwargs.get("hair_color", self.gen.hair_color())
        hair_type = kwargs.get("hair_type", self.gen.hair_type())
        eye_color = kwargs.get("eye_color", self.gen.eye_color())

        # PERSONALITY
        mannerisms = kwargs.get("mannerisms", self.gen.mannerisms())

        # LOCATIONS
        home = kwargs.get("home", self.gen.home())

        #
        ssn = kwargs.get("ssn", self.gen.ssn())
        email = Email(
            kwargs.get("email", self.gen.email(first_name, last_name, date_of_birth))
        )
        phone_number = PhoneNumber(kwargs.get("phone_number", self.gen.phone_number()))
        sexual_orientation = kwargs.get(
            "sexual_orientation", self.gen.sexual_orientation()
        )
        marital_status = kwargs.get("martial_status", "Single")

        passport_num = kwargs.get("passport_num", self.gen.passport_num())
        passport_issue_date = kwargs.get(
            "passport_issue_date", self.gen.passport_issue_date()
        )
        passport_exp_date = kwargs.get(
            "passport_exp_date",
            passport_issue_date + relativedelta(years=YEARS_TIL_PASSPORT_EXP),
        )

        # FAMILY
        siblings = kwargs.get("siblings", [])
        spouse = kwargs.get("spouse", None)

        # CAR
        vehicle = kwargs.get("vehicle", self.gen.personal_vehicle())
        drivers_license = kwargs.get("drivers_license", self.gen.drivers_license())

        return Person(
            gender=gender,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            nickname=nickname,
            title=title,
            height=height,
            weight=weight,
            hair_color=hair_color,
            hair_type=hair_type,
            eye_color=eye_color,
            mannerisms=mannerisms,
            date_of_birth=date_of_birth,
            time_of_birth=time_of_birth,
            ssn=ssn,
            email=email,
            phone_number=phone_number,
            home=home,
            vehicle=vehicle,
            drivers_license=drivers_license,
            # dl_num=dl_num,
            # dl_issue_date=dl_issue_date,
            # dl_exp_date=dl_exp_date,
            # dl_restrictions=dl_restrictions,
            sexual_orientation=sexual_orientation,
            siblings=siblings,
            marital_status=marital_status,
            passport_num=passport_num,
            passport_issue_date=passport_issue_date,
            passport_exp_date=passport_exp_date,
            spouse=spouse,
        )
