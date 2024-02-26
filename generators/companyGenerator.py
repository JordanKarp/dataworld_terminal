from faker import Faker

# from pathlib import Path

from classes.company import Company
from generator_providers.companyProvider import CompanyProvider


class CompanyGenerator:
    def __init__(self, seed=None):
        self.gen = Faker()
        if seed:
            Faker.seed(seed)
        self.gen.add_provider(CompanyProvider)
        self.id_counter = 0

    def new(self, **kwargs):
        self.id_counter += 1
        company = Company(id=f"C{self.id_counter:05d}")

        company.industry = kwargs.get("industry", self.gen.industry())
        company.sub_industry = kwargs.get(
            "sub_industry", self.gen.sub_industry(company.industry)
        )

        company.company_name = kwargs.get(
            "name", self.gen.company_name(company.industry, company.sub_industry)
        )
        company.employee_structure = kwargs.get(
            "employee_structure",
            self.gen.employee_structure(company.industry, company.sub_industry),
        )

        company.founded = kwargs.get("founded", self.gen.founded())
        company.website = kwargs.get("website", self.gen.website(company.company_name))
        company.main_phone = kwargs.get("phone_number", self.gen.company_phone_number())
        # company.locations = ["test"]
        company.social_media = ["test"]
        # company.staff = ["test"]
        # company.data = ["company_directory.txt"]

        return company
