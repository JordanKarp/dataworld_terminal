from faker import Faker
from pathlib import Path
import csv

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
        self.sources = []
        self.add_sources_from_csv(DATA_SOURCES)

    def add_sources_from_csv(self, csv_file):
        sources = load_csv(csv_file)
        for source in sources:
            self.add_data_source(source)

    def add_data_source(self, source_info):
        source_fields = source_info[1].split(",")
        ds = DataSource(source_info[0], source_fields)
        self.sources.append(ds)

    def add_population(self, pop):
        for source in self.sources:
            for person in pop:
                source.add_entry(person)

    def print_all_data_sources(self):
        for source in self.sources:
            source.print_source()

    def csv_all_data_sources(self):
        for source in self.sources:
            fields = source.fields_list
            folder = "results/"
            filename = folder + CSV_PREFIX + source.name + ".csv"
            # writing to csv file
            with open(filename, "w") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(fields)
                writer.writerows(source.data)
