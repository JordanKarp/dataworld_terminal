import csv
from pathlib import Path
from faker import Faker

# from enum import Enum, auto

from utilities.load_tools import load_csv
from classes.data_source import DataSource

# from classes.phone_number import PhoneNumber, PhoneNumberTypes
# from generator_providers.companyProvider import CompanyProvider

DATA_SOURCES = Path("./data/data_sources/sources.csv")
DATA_SOURCE_RESULTS_PATH = Path("results/sources/")


class DataSourceGenerator:
    def __init__(self, pop, comp, seed=None):
        self.gen = Faker()
        if seed:
            Faker.seed(seed)
        self.dataSources = []
        self.population = pop
        self.companies = comp
        self.load_data_sources_from_csv(DATA_SOURCES)

    def load_data_sources_from_csv(self, csv_file):
        sources = load_csv(csv_file)
        for source in sources:
            source_name = source[0]
            requirements = source[1]
            output_type = source[2]
            fields = source[3].split(",")

            ds = DataSource(source_name, requirements, output_type, fields)
            self.dataSources.append(ds)

    # def add_company_directories(self):
    #     for c in self.companies:
    #         if c.num_employees_hired:
    #             pass  # Add company directories logic here

    def generate_data_source_lists(self, output="CSV"):
        for source in self.dataSources:
            for p in self.population:
                source.add_entry(p)
            for c in self.companies:
                source.add_entry(c)
        if output == "CSV":
            self.csv_all_data_sources()
        elif output == "PRINT":
            self.print_all_data_sources()

    def print_all_data_sources(self):
        for source in self.dataSources:
            source.print_source()

    def csv_all_data_sources(self):
        for source in self.dataSources:
            filename = DATA_SOURCE_RESULTS_PATH / f"{source.name}.csv"
            data = [
                row
                for row in source.data
                if not all(element.isspace() for element in row)
            ]
            with open(filename, "w") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(source.fields)
                writer.writerows(data)
