from faker import Faker
from pathlib import Path

from classes.company import Company
from classes.phone_number import PhoneNumber, PhoneNumberTypes
from generator_providers.companyProvider import CompanyProvider


class CompanyGenerator:
    def __init__(self, seed=None):
        self.gen = Faker()
        if seed:
            Faker.seed(seed)
        self.gen.add_provider(CompanyProvider)

    def new_company(self, **kwargs):
        industry = kwargs.get("industry", self.gen.industry())
        sub_industry = kwargs.get("sub_industry", self.gen.sub_industry(industry))

        name = kwargs.get("name", self.gen.company_name(sub_industry))
        website = kwargs.get("website", self.gen.website(name))
        sub_industry = "test"
        main_phone = kwargs.get("phone_number", self.gen.company_phone_number())
        # locations = ["test"]
        social_media = ["test"]
        # staff = ["test"]
        data = ["company_directory.txt"]

        return Company(
            name=name,
            website=website,
            industry=industry,
            sub_industry=sub_industry,
            main_phone=main_phone,
            # locations=locations,
            social_media=social_media,
            # staff=staff,
            data=data,
        )
