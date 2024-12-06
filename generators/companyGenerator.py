from faker import Faker

# from pathlib import Path

from classes.company import Company
from classes.employee import WorkLocation
from generator_providers.companyProvider import CompanyProvider
from generator_providers.locationProvider import LocationProvider
from generator_providers.documentProvider import DocumentProvider


class CompanyGenerator:
    def __init__(self, seed=None, locations=[]):
        self.gen = Faker()
        if seed:
            Faker.seed(seed)
        self.locations = locations
        self.gen.add_provider(CompanyProvider)
        # self.gen.add_provider(LocationProvider)
        self.gen.add_provider(DocumentProvider)
        self.id_counter = 0

    def new(self, **kwargs):
        self.id_counter += 1
        company = Company(id=f"C{self.id_counter:05d}")

        industry = kwargs.get("industry", self.gen.industry())
        company.industry = industry

        name = kwargs.get("name", self.gen.name(industry))
        company.name = name
        company.slogan = kwargs.get("name", self.gen.slogan(industry))
        company.opener = kwargs.get("name", self.gen.opener(industry, name))
        company.products = kwargs.get("name", self.gen.products(industry))
        # company.employee_structure = kwargs.get(
        #     "employee_structure",
        #     self.gen.employee_structure(company.industry, company.sub_industry),
        # )

        company.founded = kwargs.get("founded", self.gen.founded())
        company.website_font_color = kwargs.get(
            "website_font_color", self.gen.website_font_color()
        )
        company.main_phone = kwargs.get("phone_number", self.gen.company_phone_number())
        bank_account_amount = kwargs.get(
            "bank_account_amount", self.gen.bank_account_amount(20000, 1000000)
        )
        company.bank_account = kwargs.get(
            "bank_account", self.gen.bank_account(bank_account_amount)
        )
        scope = kwargs.get("cliet_scope", self.gen.client_scope(industry))
        company.client_scope = scope
        # company.social_media = ["test"]

        location_types = kwargs.get(
            "locations_types",
            self.gen.locations_info(industry, scope),
        )
        locations = []
        for loc_id, loc_data in location_types.items():
            num_loc_of_type = self.gen.random_int(
                loc_data["LOCATION_RANGE"][0], loc_data["LOCATION_RANGE"][1]
            )
            for _ in range(num_loc_of_type):
                loc = self.get_location(loc_data["LOCATION_TYPE"])
                employees = self.gen.employee_structure(industry, scope, loc_id)
            locations.append(WorkLocation(loc, employees, loc_id))
        company.locations = locations
        # company.market_share = kwargs.get(
        #     "market_share",
        #     self.gen.market_share(company.industry, company.sub_industry),
        # )

        # company.data = ["company_directory.txt"]

        return company

    def get_location(self, loc_type):
        locs = [loc for loc in self.locations if loc and loc.building_type == loc_type]

        loc = self.gen.random_element(locs)
        self.locations.remove(loc)
        return loc
