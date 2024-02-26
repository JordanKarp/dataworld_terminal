import csv
from pathlib import Path

from generators.companyGenerator import CompanyGenerator

# from utilities.load_tools import load_weighted_csv

EXPORT_CSV_NAME = Path("results/TestCompanies.csv")

FIRST_PASS_COMPANIES = 10
EMPLOYED_PERCENT = 0.85


class CompaniesGenerator:
    def __init__(self, seed=None) -> None:
        self.seed = seed
        self.companyGen = CompanyGenerator(self.seed)
        self.all_companies = []
        self.population = []

    def create(self):
        self.initial_companies(FIRST_PASS_COMPANIES)
        return self.all_companies

    def initial_companies(self, num_companies):
        for _ in range(num_companies):
            self.all_companies.append(self.companyGen.new())

    def load_population(self, population):
        self.population = population

    def add_employees(self):
        employable_people = [
            p for p in self.population if p.can_work and not p.is_working
        ]
        hiring_companies = [c for c in self.all_companies if c.room_to_hire]
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

    def print_eco(self):
        for company in self.all_companies:
            print(company)

    def csv_eco(self, filename=EXPORT_CSV_NAME):
        if self.all_companies:
            with open(filename, "w") as csvfile:
                writer = csv.writer(csvfile)
                # header
                writer.writerow(
                    [
                        k
                        for k in self.all_companies[0].__dict__.keys()
                        if not k.startswith("__")
                    ]
                )
                # rows
                writer.writerows(self.all_companies)
