from csv import DictWriter
from pathlib import Path
from datetime import date
from random import choices

from classes.person import Person
from generators.personGenerator import PersonGenerator
from generator_utilities.load_tools import load_weighted_csv

FIRST_PASS_POP_SIZE = 10
SIBLING_DATA_PATH = Path("data/population/num_children_weights.csv")

EXPORT_CSV_NAME = f"TestPopulation - {date.today()}.csv"


class PopulationGenerator:
    def __init__(self, seed=None) -> None:
        self.seed = seed
        self.personGen = PersonGenerator(self.seed)
        self.population = []

    def create(self):
        self.initial_pop()
        self.add_siblings()

    def initial_pop(self):
        for i in range(FIRST_PASS_POP_SIZE):
            self.population.append(self.personGen.new())

    def add_siblings(self):
        sib_nums, sib_weights = load_weighted_csv(SIBLING_DATA_PATH)
        new_pop = []
        for person in self.population:
            numSibs = int(choices(sib_nums, sib_weights)[0])

            if numSibs:
                family = [person]
                for _ in range(numSibs):
                    new = self.personGen.new(last_name=person.last_name)
                    family.append(new)
                    new_pop.append(new)
                for p in family:
                    p.siblings = [sib for sib in family if sib != p]
            else:
                person.siblings = []
        self.population.extend(new_pop)

    def add_spouses(self):
        pass

    def print_pop(self):
        for person in self.population:
            print(person)

    def csv_pop(self, filename=EXPORT_CSV_NAME):
        fields = [k for k in Person.__dict__.keys() if not k.startswith("__")]
        # fields = [k for k, v in Person.__dict__.items()]
        # print(fields)

        # writing to csv file
        with open(filename, "w") as csvfile:
            # creating a csv dict writer object
            fields = [
                k for k in self.population[0].__dict__.keys() if not k.startswith("__")
            ]
            writer = DictWriter(csvfile, fieldnames=fields)

            # writing headers (field names)
            writer.writeheader()

            # writing data rows
            for person in self.population:
                writer.writerow(
                    {k: v for k, v in person.__dict__.items() if k in fields}
                )
