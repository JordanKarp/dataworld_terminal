from random import choice, choices
from faker import Faker
from faker.providers import BaseProvider
from pathlib import Path

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

HAIR_COLORS_PATH = Path("./data/person/hair_color_weights.csv")
HAIR_TYPES_PATH = Path("./data/person/hair_types.txt")
EYE_COLORS_PATH = Path("./data/person/eye_color_weights.csv")
GENDER_PATH = Path("./data/person/gender_weights.csv")
SEXUAL_ORIENTATION_PATH = Path("./data/person/sexual_orientation_weights.csv")
# POSITIVE_TRAITS_PATH = Path("./data/person/positive_traits.txt")
# NEUTRAL_TRAITS_PATH = Path("./data/person/neutral_traits.txt")
# NEGATIVE_TRAITS_PATH = Path("./data/person/negative_traits.txt")
MANNERISMS_PATH = Path("./data/person/mannerisms.txt")


class PersonalDetailsProvider(BaseProvider):
    gen = Faker()

    hair_colors, hair_color_weights = load_weighted_csv(HAIR_COLORS_PATH)
    hair_types = load_txt(HAIR_TYPES_PATH)
    eye_colors, eye_color_weights = load_weighted_csv(EYE_COLORS_PATH)
    genders, gender_weights = load_weighted_csv(GENDER_PATH)
    mannerisms_options = load_txt(MANNERISMS_PATH)

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

    def mannerisms(self):
        return choice(self.mannerisms_options)

    def email(self, first, last, dob):
        year = str(dob.year)[2:]
        md = str(dob.month) + str(dob.day)
        options = [
            first + last,
            first[0] + last,
            first + last + str(self.gen.random_int(max=99)),
            first[0] + last + str(self.gen.random_int(max=99)),
            first + last + year,
            first[0] + last + year,
            first + last + md,
            first[0] + last + md,
        ]
        return choice(options).lower() + "@" + self.gen.free_email_domain()

    def phone_number(self):
        return self.gen.numerify(text="(%#%) %##-####")
