from pathlib import Path
from faker import Faker
from collections import defaultdict
from generators.companyGenerator import CompanyGenerator
from generator_providers.personFilters import (
    get_regional_pop,
    get_state_pop,
    get_gendered_pop,
    get_pop_with_siblings,
)
from utilities.load_tools import load_json

EXPORT_CSV_NAME = Path("results/TestCompanies.csv")

FIRST_PASS_COMPANIES = 80
EMPLOYED_PERCENT = 1


class CompaniesGenerator:
    def __init__(self, seed=None, locations=[]) -> None:
        self.gen = Faker()
        if seed:
            Faker.seed(seed)
        self.locations = locations
        self.companyGen = CompanyGenerator(seed, self.locations)
        self.all_companies = {}
        self.population = {}

    def create(self, initial_companies=FIRST_PASS_COMPANIES):
        self.initial_companies(initial_companies)
        return self.all_companies

    def initial_companies(self, num_companies):
        for _ in range(num_companies):
            c = self.companyGen.new()
            self.all_companies[c.id] = c

    def load_population(self, population):
        self.population = population

    def add_employees(self):
        employable_people = [
            p for p in self.population.values() if p.can_work and not p.is_working
        ]
        hiring_companies = [c for c in self.all_companies.values() if c.room_to_hire]
        # print(hiring_companies)
        for person in employable_people:
            if hiring_companies and self.companyGen.gen.percent_check(EMPLOYED_PERCENT):
                comp = self.companyGen.gen.random_element(hiring_companies)
                comp.add_employee(person)
                if not comp.room_to_hire:
                    hiring_companies.remove(comp)
            else:
                person.role = "Unemployed"
                person.salary = 0
                person.work_days = []
                person.work_hours = []
        return self.all_companies

    def _get_scopes(self, population, company):
        return {
            "National": population,
            "Online": population,
            "Regional": get_regional_pop(company.zip_codes, population),
            "Local": get_state_pop(company.states, population),
            "Female": get_gendered_pop("Female", population),
            "Male": get_gendered_pop("Male", population),
            # "Has_siblings": get_pop_with_siblings(population),
        }

    def add_clients(self):
        potential_clients = [p for p in self.population.values() if p.can_work]
        for company in self.all_companies.values():
            scopes = self._get_scopes(potential_clients, company)
            for person in scopes[company.client_scope]:
                if self.companyGen.gen.percent_check(company.market_share):
                    company.add_client(person)

    def add_favorite_companies(self):
        industries = {company.industry for company in self.all_companies.values()}
        eligible_people = [p for p in self.population.values() if p.bank_account]
        for person in eligible_people:
            for industry in industries:
                fav = self.gen.random_element(self._companies_in_industry(industry))
                freq = self.companyGen.gen.client_frequency(industry)
                # print(freq)
                person.favorites[industry] = (fav.id, freq)
                # print(
                #     f"{person}'s favorite {industry} is {fav.name} and they go ~{freq * 365} times a year"
                # )

    def _companies_in_industry(self, industry=None):
        if not industry:
            return self.all_companies.values()
        return [c for c in self.all_companies.values() if c.industry == industry]

    def return_companies(self):
        return self.all_companies
