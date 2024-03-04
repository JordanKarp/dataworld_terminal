from faker import Faker

# from pathlib import Path

from classes.company import Company
from generator_providers.companyProvider import CompanyProvider
from generator_providers.locationProvider import LocationProvider


class CompanyGenerator:
    def __init__(self, seed=None):
        self.gen = Faker()
        if seed:
            Faker.seed(seed)
        self.gen.add_provider(CompanyProvider)
        self.gen.add_provider(LocationProvider)
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
        company.client_scope = kwargs.get(
            "cliet_scope", self.gen.client_scope(company.industry, company.sub_industry)
        )
        # company.social_media = ["test"]
        # company.locations = kwargs.get(
        #     "locations",
        #     self.gen.company_locations(),
        # )
        company.hq = kwargs.get("hq", self.gen.company_hq())
        company.market_share = kwargs.get(
            "market_share",
            self.gen.market_share(company.industry, company.sub_industry),
        )

        # company.data = ["company_directory.txt"]

        return company
