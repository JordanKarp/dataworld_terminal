from faker import Faker
from faker.providers import BaseProvider
from generator_providers.choicesProvider import ChoicesProvider

from pathlib import Path


from generator_utilities.load_tools import load_weighted_csv

DOMAINS_PATH = Path("./data/internet/domains_weights.csv")

# ALL_CHAR_NUM = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


class InternetProvider(BaseProvider):
    gen = Faker()
    gen.add_provider(ChoicesProvider)

    domains, domain_weights = load_weighted_csv(DOMAINS_PATH)

    def email(self, first, last, dob):
        return f"{self.user_name(first, last, dob)}@{self.email_domain()}"

    def user_name(self, first, last, dob):
        year = str(dob.year)[2:]
        md = str(dob.month) + str(dob.day)
        options = [
            last + str(self.gen.random_int(max=999)),
            first + last,
            first[0] + last,
            first + last + str(self.gen.random_int(max=999)),
            first[0] + last + str(self.gen.random_int(max=999)),
            first + last + year,
            first[0] + last + year,
            first + last + md,
            first[0] + last + md,
        ]
        return self.gen.random_element(options).lower()

    def email_domain(self):
        return self.gen.weighted_choice(self.domains, self.domain_weights)
