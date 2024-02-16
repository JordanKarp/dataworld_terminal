from faker import Faker
from faker.providers import BaseProvider

from classes.company import Industries
from classes.phone_number import PhoneNumber, PhoneNumberTypes

# from generator_utilities.load_tools import load_weighted_csv

# DOMAINS_PATH = Path("./data/internet/domains_weights.csv")

# ALL_CHAR_NUM = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


class CompanyProvider(BaseProvider):
    gen = Faker()

    def company_name(self, sub_industry):
        return "Food Inc"

    def industry(self):
        return self.gen.random_element(Industries)

    def sub_industry(self, industry):
        return "elem"

    def website(self, company_name, domain_suff="com"):
        secure = "s" if self.gen.pybool() is True else ""
        name_str = "".join(company_name.split(" "))
        return f"http{secure}://www.{name_str.lower()}.{domain_suff}"

    def company_phone_number(self):
        return PhoneNumber(
            self.gen.numerify(text="(%#%) %##-####"), PhoneNumberTypes.WORK
        )
