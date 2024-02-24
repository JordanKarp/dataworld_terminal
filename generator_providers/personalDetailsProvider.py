from datetime import date
from dateutil.relativedelta import relativedelta

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
# POSITIVE_TRAITS_PATH = Path("./data/person/positive_traits.txt")
# NEUTRAL_TRAITS_PATH = Path("./data/person/neutral_traits.txt")
# NEGATIVE_TRAITS_PATH = Path("./data/person/negative_traits.txt")
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
    sexual_orientations, sexual_orientation_weights = load_weighted_csv(
        SEXUAL_ORIENTATION_PATH
    )

    def gender(self):
        return self.weighted_choice(self.genders, self.gender_weights)

    def first_name_gender(self, gender):
        if gender == "Male":
            return self.generator.first_name_male()
        elif gender == "Female":
            return self.generator.first_name_female()
        else:
            return self.generator.first_name_nonbinary()

    def middle_name_gender(self, gender):
        name = ""
        if gender == "Male":
            name = self.generator.first_name_male()
        elif gender == "Female":
            name = self.generator.first_name_female()
        else:
            name = self.generator.first_name_nonbinary()
        return self.blank_or(name, MIDDLE_NAME_PERC)

    def age(self, date_of_birth, date_of_death=None):
        upper_date = date_of_death or self.generator.today()
        return (
            upper_date.year
            - date_of_birth.year
            - (
                (upper_date.month, upper_date.day)
                < (date_of_birth.month, date_of_birth.day)
            )
        )

    def date_of_birth_generation(self, generation=0):
        years_ago = self.generator.random_int(
            generation * 20 + 1, (generation + 1) * 20
        )
        year = self.generator.today().year - years_ago
        return self.generator.date_between(date(year, 1, 1), date(year, 12, 31))

    def time_of_birth(self):
        return self.generator.time(pattern="%I:%M %p")

    # def is_alive(self, age):
    #     return self.generator.random_int(0, 100) > age * DEATH_AGE_FACTOR

    def date_of_death(self, date_of_birth, generation=0):
        theoretical_age = int(self.generator.today().year - date_of_birth.year)
        death_pct = self.generator.random_int(0, 100)
        if death_pct > theoretical_age * DEATH_AGE_FACTOR:
            return None
        death_age = min(
            theoretical_age,
            int(self.norm_dist_rand(DEATH_AGE_MEAN - generation, DEATH_AGE_STDEV)),
        )
        return min(
            self.generator.today(),
            self.generator.random_date_margin(
                date_of_birth + relativedelta(years=death_age), 0, 1
            ),
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

    def mannerisms(self):
        return self.generator.random_element(self.mannerisms_options)

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
