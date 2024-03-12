from datetime import date
from dateutil.relativedelta import relativedelta
from itertools import product

from pathlib import Path

from classes.phone_number import PhoneNumber
from generator_providers.choicesProvider import ChoicesProvider
from generator_providers.dateProvider import DateProvider
from utilities.load_tools import load_txt, load_weighted_csv, load_csv_as_dict

from data.person.person_averages import (
    MENS_H_MEAN,
    MENS_H_STDEV,
    WOMENS_H_MEAN,
    WOMENS_H_STDEV,
    MENS_W_MEAN,
    MENS_W_STDEV,
    WOMENS_W_MEAN,
    WOMENS_W_STDEV,
    MIDDLE_NAME_PERC,
)

GENERATION_DELTA = 20
BIRTHDAY_YEAR_DELTA = 10
NICKNAME_PCT_CHANCE = 0.6
DEATH_AGE_FACTOR = 0.80
DEATH_AGE_MEAN = 80
DEATH_AGE_STDEV = 10

HAIR_COLORS_PATH = Path("./data/person/hair_color_weights.csv")
HAIR_TYPES_PATH = Path("./data/person/hair_types.txt")
EYE_COLORS_PATH = Path("./data/person/eye_color_weights.csv")
GENDER_PATH = Path("./data/person/gender_weights.csv")
SEXUAL_ORIENTATION_PATH = Path("./data/person/sexual_orientation_weights.csv")
POSITIVE_TRAITS_PATH = Path("./data/person/positive_traits.txt")
NEUTRAL_TRAITS_PATH = Path("./data/person/neutral_traits.txt")
NEGATIVE_TRAITS_PATH = Path("./data/person/negative_traits.txt")
MANNERISMS_PATH = Path("./data/person/mannerisms.txt")
AGES_PATH = Path("./data/person/age_weights.csv")
NICKNAMES_PATH = Path("./data/person/names.csv")


class PersonalDetailsProvider(ChoicesProvider, DateProvider):

    genders, gender_weights = load_weighted_csv(GENDER_PATH)
    ages, ages_weights = load_weighted_csv(AGES_PATH)
    nicknames_dict = load_csv_as_dict(NICKNAMES_PATH)

    hair_colors, hair_color_weights = load_weighted_csv(HAIR_COLORS_PATH)
    hair_types = load_txt(HAIR_TYPES_PATH)
    eye_colors, eye_color_weights = load_weighted_csv(EYE_COLORS_PATH)
    mannerisms_options = load_txt(MANNERISMS_PATH)
    positive_traits = load_txt(POSITIVE_TRAITS_PATH)
    neutral_traits = load_txt(NEUTRAL_TRAITS_PATH)
    negative_traits = load_txt(NEGATIVE_TRAITS_PATH)
    sexual_orientations, sexual_orientation_weights = load_weighted_csv(
        SEXUAL_ORIENTATION_PATH
    )

    def gender(self):
        return self.weighted_choice(self.genders, self.gender_weights)

    def first_name_gender(self, gender):
        return {
            "Male": self.generator.first_name_male,
            "Female": self.generator.first_name_female,
            "Nonbinary": self.generator.first_name_nonbinary,
        }.get(gender, self.generator.first_name_nonbinary)()

    def middle_name_gender(self, gender):
        name = self.first_name_gender(gender)
        return self.blank_or(name, MIDDLE_NAME_PERC)

    def custom_last_name(self, name=None):
        return name if name is not None else self.generator.last_name()

    def _calculate_age(self, date_of_birth, upper_date):
        return (
            upper_date.year
            - date_of_birth.year
            - (
                (upper_date.month, upper_date.day)
                < (date_of_birth.month, date_of_birth.day)
            )
        )

    def age(self, date_of_birth, date_of_death=None):
        upper_date = date_of_death or self.generator.today()
        return self._calculate_age(date_of_birth, upper_date)

    def date_of_birth_generation(self, generation=0):
        start_year = self.generator.today().year - (generation + 1) * GENERATION_DELTA
        end_year = start_year + GENERATION_DELTA
        return self.generator.date_between_dates(
            date(start_year, 1, 1), date(end_year, 12, 31)
        )

    def time_of_birth(self):
        return self.generator.time(pattern="%I:%M %p")

    def date_of_death(self, date_of_birth, generation=0):
        theoretical_age = int(self.generator.today().year - date_of_birth.year)
        death_pct = self.generator.random_int(0, 100)
        if death_pct > theoretical_age * DEATH_AGE_FACTOR:
            return None
        death_age = max(
            0,
            min(
                theoretical_age,
                int(self.norm_dist_rand(DEATH_AGE_MEAN - generation, DEATH_AGE_STDEV)),
            ),
        )

        death_date = date_of_birth + relativedelta(years=death_age)
        return min(
            self.generator.today(),
            self.generator.random_date_margin(death_date, 0, 1),
        )

    def height(self, gender):
        gender_heights = {
            "Male": (MENS_H_MEAN, MENS_H_STDEV),
            "Female": (WOMENS_H_MEAN, WOMENS_H_STDEV),
        }
        mean, stdev = gender_heights.get(gender, (WOMENS_H_MEAN, WOMENS_H_STDEV))
        return round(self.generator.norm_dist_rand(mean, stdev), 1)

    def weight(self, gender):
        gender_weights = {
            "Male": (MENS_W_MEAN, MENS_W_STDEV),
            "Female": (WOMENS_W_MEAN, WOMENS_W_STDEV),
        }
        mean, stdev = gender_weights.get(gender, (WOMENS_W_MEAN, WOMENS_W_STDEV))
        return round(self.generator.norm_dist_rand(mean, stdev), 1)

    def hair_color(self):
        return self.weighted_choice(self.hair_colors, self.hair_color_weights)

    def hair_type(self):
        return self.generator.random_element(self.hair_types)

    def eye_color(self):
        return self.weighted_choice(self.eye_colors, self.eye_color_weights)

    def sexual_orientation(self):
        return self.weighted_choice(
            self.sexual_orientations, self.sexual_orientation_weights
        )

    def blood_type_allele(self, person_a=None, person_b=None):
        if person_a is None or person_b is None:
            return "".join(
                self.random_element(
                    product(["AA", "AO", "BB", "BO", "AB", "OO"], ["DD", "Dd", "dd"])
                )
            )

        abo_options = (
            person_a.blood_type_allele[0] + person_b.blood_type_allele[0],
            person_a.blood_type_allele[1] + person_b.blood_type_allele[1],
        )
        rh_options = (
            person_a.blood_type_allele[2] + person_b.blood_type_allele[2],
            person_a.blood_type_allele[3] + person_b.blood_type_allele[3],
        )
        options = [a1 + a2 for a1 in abo_options for a2 in rh_options]

        frequency_count = {}
        for option in options:
            frequency_count[option] = frequency_count.get(option, 0) + 1
        return self.weighted_choice(frequency_count.keys(), frequency_count.values())

    def mannerisms(self):
        return self.generator.random_element(self.mannerisms_options)

    def traits(self, trait_type, k=1):
        if trait_type == "positive":
            traits = self.positive_traits
        elif trait_type == "neutral":
            traits = self.neutral_traits
        elif trait_type == "negative":
            traits = self.negative_traits
        return ", ".join(self.generator.random_elements(traits, length=k, unique=True))

    def phone_number(self):
        return PhoneNumber(self.generator.numerify(text="(%#%) %##-####"))

    def nickname(self, first_name, middle_name=None):
        options = [
            nickname.title()
            for name in [first_name, middle_name]
            if name and name.lower() in self.nicknames_dict
            for nickname in self.nicknames_dict[name.lower()]
        ]
        return (
            self.generator.blank_or(
                self.generator.random_element(options), NICKNAME_PCT_CHANCE
            )
            if options
            else ""
        )
