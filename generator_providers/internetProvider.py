from pathlib import Path

from classes.email import Email, EmailTypes
from generator_providers.choicesProvider import ChoicesProvider

from utilities.load_tools import load_weighted_csv

DOMAINS_PATH = Path("./data/internet/domains_weights.csv")


class InternetProvider(ChoicesProvider):
    domains, domain_weights = load_weighted_csv(DOMAINS_PATH)

    def email(self, first, last, dob):
        return Email(
            f"{self.user_name(first, last, dob)}@{self.email_domain()}",
            EmailTypes.PERSONAL,
        )

    def user_name(self, first, last, dob):
        year = str(dob.year)[2:]
        md = str(dob.month) + str(dob.day)
        options = [
            last + str(self.generator.random_int(max=999)),
            first + last,
            first[0] + last,
            first + last + str(self.generator.random_int(max=999)),
            first[0] + last + str(self.generator.random_int(max=999)),
            first + last + year,
            first[0] + last + year,
            first + last + md,
            first[0] + last + md,
        ]
        return self.generator.random_element(options).lower()

    def email_domain(self):
        return self.generator.weighted_choice(self.domains, self.domain_weights)
