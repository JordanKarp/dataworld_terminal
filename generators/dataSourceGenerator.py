from faker import Faker
from pathlib import Path
import csv
from enum import Enum, auto

from utilities.load_tools import load_csv
from classes.data_source import DataSource

# from classes.phone_number import PhoneNumber, PhoneNumberTypes
# from generator_providers.companyProvider import CompanyProvider

DATA_SOURCES = Path("./data/data_sources/sources.csv")
CSV_PREFIX = "DS-"


class DataSourceGenerator:
    def __init__(self, seed=None):
        self.gen = Faker()
        if seed:
            Faker.seed(seed)
        self.dataSources = []
        self.add_data_sources_from_csv(DATA_SOURCES)

    def add_data_sources_from_csv(self, csv_file):
        sources = load_csv(csv_file)
        for source in sources:
            source_name = source[0]
            source_type = source[1]
            source_fields = source[2].split(",")
            ds = DataSource(source_name, source_fields)

    def add_population(self, pop):
        for source in self.dataSources:
            for person in pop:
                source.add_entry(person)

    def add_companies(self, companies):
        for source in self.dataSources:
            for comp in companies:
                source.add_entry(comp)

    def print_all_data_sources(self):
        for source in self.dataSources:
            source.print_source()

    def csv_all_data_sources(self):
        folder = Path("results/")
        for source in self.dataSources:
            fields = source.fields_list
            filename = folder / f"{CSV_PREFIX}{source.name}.csv"
            # writing to csv file
            with open(filename, "w") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(fields)
                data = [
                    row
                    for row in source.data
                    if not all(element.isspace() for element in row)
                ]
                writer.writerows(data)
