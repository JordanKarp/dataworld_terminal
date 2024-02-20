import csv
from csv import DictWriter
from pathlib import Path

# from dataclasses import asdict, astuple

# from datetime import date


from classes.company import Company
from generators.companyGenerator import CompanyGenerator

# from generator_utilities.load_tools import load_weighted_csv

# FIRST_PASS_POP_SIZE = 5
# MINIMUM_MARRIAGE_AGE = 18
# SIBLING_DATA_PATH = Path("data/population/num_children_weights.csv")
# MARRIAGE_RATE_PATH = Path("data/population/marrage_rates_weights.csv")

EXPORT_CSV_NAME = Path("results/TestCompanies.csv")

FIRST_PASS_COMPANIES = 4


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
        pass
        # fields = [k for k in self.all_companies[0] if not k.startswith("__")]
        # print(Company.__dict__.keys())
        # # writing to csv file
        # with open(filename, "w") as csvfile:
        #     # creating a csv dict writer object
        #     writer = DictWriter(csvfile, fieldnames=fields)
        #     # writing headers (field names)
        #     writer.writeheader()
        #     # writing data rows
        #     for company in self.all_companies:
        #         writer.writerow(
        #             {k: v for k, v in company.__dict__.items() if k in fields}
        #         )
