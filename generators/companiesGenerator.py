import csv
from pathlib import Path

from generators.companyGenerator import CompanyGenerator

# from utilities.load_tools import load_weighted_csv

EXPORT_CSV_NAME = Path("results/TestCompanies.csv")

FIRST_PASS_COMPANIES = 80
EMPLOYED_PERCENT = 0.85


class CompaniesGenerator:
    def __init__(self, seed=None) -> None:
        self.seed = seed
        self.companyGen = CompanyGenerator(self.seed)
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
        for person in employable_people:
            if hiring_companies and self.companyGen.gen.percent_check(EMPLOYED_PERCENT):
                comp = self.companyGen.gen.random_element(hiring_companies)
                person.role = comp.add_employee(person)
                person.employer = comp
                if not comp.room_to_hire:
                    hiring_companies.remove(comp)
            else:
                person.role = "Unemployed"
        return self.all_companies

    def _get_scopes(self, potential_clients, company):
        local_cond = lambda p: p.home and p.home.state == company.hq.state
        regional_cond = lambda p: p.home and p.home.zipcode[0] == company.hq.zipcode[0]
        gender_cond = lambda p, gender: p.gender == gender

        return {
            "National": potential_clients,
            "Online": potential_clients,
            "Regional": [p for p in potential_clients if regional_cond(p)],
            "Local": [p for p in potential_clients if local_cond(p)],
            "Female": [p for p in potential_clients if gender_cond(p, "Female")],
            "Male": [p for p in potential_clients if gender_cond(p, "Male")],
            # "Male": gender_cond("Male"),
        }

    def add_clients(self):
        potential_clients = [p for p in self.population.values() if p.can_work]
        for company in self.all_companies.values():
            scopes = self._get_scopes(potential_clients, company)
            for person in scopes[company.client_scope]:
                if self.companyGen.gen.percent_check(company.market_share):
                    company.add_client(person)

    def return_companies(self):
        return self.all_companies
