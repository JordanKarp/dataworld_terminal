import csv
from csv import DictWriter
from pathlib import Path

from generators.companyGenerator import CompanyGenerator

# from utilities.load_tools import load_weighted_csv

EXPORT_CSV_NAME = Path("results/TestCompanies.csv")

FIRST_PASS_COMPANIES = 500


class EconomyGenerator:
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
