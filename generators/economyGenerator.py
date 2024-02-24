import csv
from pathlib import Path

from generators.companyGenerator import CompanyGenerator

# from utilities.load_tools import load_weighted_csv

EXPORT_CSV_NAME = Path("results/TestCompanies.csv")

FIRST_PASS_COMPANIES = 30
EMPLOYED_PERCENT = 0.85


class CompaniesGenerator:
    def __init__(self, seed=None) -> None:
        self.seed = seed
        self.companyGen = CompanyGenerator(self.seed)
        self.all_companies = []

    def create(self):
        self.initial_companies(FIRST_PASS_COMPANIES)
        return self.all_companies

    def initial_companies(self, num_companies):
        for _ in range(num_companies):
            self.all_companies.append(self.companyGen.new())

    def add_employees(self, population):
        companies_with_room = [
            comp for comp in self.all_companies if comp.room_to_hire > 0
        ]
        for person in population:
            if (
                person.can_work
                and not person.is_working
                and self.companyGen.gen.random_int(0, 100) <= (100 * EMPLOYED_PERCENT)
            ):
                comp = self.companyGen.gen.random_element(companies_with_room)
                person.role = comp.add_employee(person)
                person.employer = comp
            else:
                person.role = "Unemployed"

    # def add_employees(self, population):
    #     for person in population:
    #         if person.can_work and not person.is_working:
    #             comp = self.companyGen.gen.random_element(self.all_companies)
    #             while comp.room_to_hire <= 0:
    #                 comp = self.companyGen.gen.random_element(self.all_companies)

    #             person.role = comp.add_employee(person)
    #             person.employer = comp

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
