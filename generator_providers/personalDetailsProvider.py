from datetime import date
from faker import Faker
from faker.providers import BaseProvider
from pathlib import Path
from random import choice, choices, randint


from generator_utilities.load_tools import load_txt, load_weighted_csv
from generator_utilities.random_tools import norm_dist_rand
from data.person.person_averages import (
    MENS_H_MEAN,
    MENS_H_STDEV,
    WOMENS_H_MEAN,
    WOMENS_H_STDEV,
    MENS_W_MEAN,
    MENS_W_STDEV,
    WOMENS_W_MEAN,
    WOMENS_W_STDEV,
)

BIRTHDAY_YEAR_DELTA = 10


HAIR_COLORS_PATH = Path("./data/person/hair_color_weights.csv")
HAIR_TYPES_PATH = Path("./data/person/hair_types.txt")
EYE_COLORS_PATH = Path("./data/person/eye_color_weights.csv")
GENDER_PATH = Path("./data/person/gender_weights.csv")
SEXUAL_ORIENTATION_PATH = Path("./data/person/sexual_orientation_weights.csv")
# POSITIVE_TRAITS_PATH = Path("./data/person/positive_traits.txt")
# NEUTRAL_TRAITS_PATH = Path("./data/person/neutral_traits.txt")
# NEGATIVE_TRAITS_PATH = Path("./data/person/negative_traits.txt")
MANNERISMS_PATH = Path("./data/person/mannerisms.txt")
AGES_PATH = Path("./data/person/age_weights.csv")


class PersonalDetailsProvider(BaseProvider):
    gen = Faker()

    hair_colors, hair_color_weights = load_weighted_csv(HAIR_COLORS_PATH)
    hair_types = load_txt(HAIR_TYPES_PATH)
    eye_colors, eye_color_weights = load_weighted_csv(EYE_COLORS_PATH)
    genders, gender_weights = load_weighted_csv(GENDER_PATH)
    mannerisms_options = load_txt(MANNERISMS_PATH)
    sexual_orientations, sexual_orientation_weights = load_weighted_csv(
        SEXUAL_ORIENTATION_PATH
    )
    ages, ages_weights = load_weighted_csv(AGES_PATH)

    def birthday(self, starting_dob):
        if starting_dob:
            start_year = starting_dob.year
            bd = self.gen.date_between_dates(
                date(
                    start_year - BIRTHDAY_YEAR_DELTA,
                    starting_dob.month,
                    starting_dob.day,
                ),
                date(
                    start_year + BIRTHDAY_YEAR_DELTA,
                    starting_dob.month,
                    starting_dob.day,
                ),
            )
        else:
            start_year = date.today().year
            min_age, max_age = choices(self.ages, self.ages_weights)[0].split("-")
            year_delta = randint(int(min_age), int(max_age))
            bd = self.gen.date_between_dates(
                date(start_year, 1, 1), date(start_year, 12, 31)
            )
            bd = bd.replace(year=(start_year - year_delta))
        return bd

    def gender(self):
        return choices(self.genders, self.gender_weights)[0]

    def height(self):
        if self.gender == "Male":
            return round(norm_dist_rand(MENS_H_MEAN, MENS_H_STDEV), 1)
        else:
            return round(norm_dist_rand(WOMENS_H_MEAN, WOMENS_H_STDEV), 1)

    def weight(self):
        if self.gender == "Male":
            return round(norm_dist_rand(MENS_W_MEAN, MENS_W_STDEV), 1)
        else:
            return round(norm_dist_rand(WOMENS_W_MEAN, WOMENS_W_STDEV), 1)

    def hair_color(self):
        return choices(self.hair_colors, self.hair_color_weights)[0]

    def hair_type(self):
        return choice(self.hair_types)

    def eye_color(self):
        return choices(self.eye_colors, self.eye_color_weights)[0]

    def sexual_orientation(self):
        return choices(self.sexual_orientations, self.sexual_orientation_weights)[0]

    def mannerisms(self):
        return choice(self.mannerisms_options)

    def phone_number(self):
        return self.gen.numerify(text="(%#%) %##-####")
