from csv import DictWriter
from pathlib import Path


from classes.person import Person
from generators.personGenerator import PersonGenerator
from utilities.load_tools import load_weighted_csv

FIRST_PASS_POP_SIZE = 100
MINIMUM_MARRIAGE_AGE = 18
SIBLING_DATA_PATH = Path("data/population/num_children_weights.csv")
MARRIAGE_RATE_PATH = Path("data/population/marrage_rates_weights.csv")

EXPORT_CSV_NAME = "results/TestPopulation.csv"


class PopulationGenerator:
    def __init__(self, seed=None) -> None:
        self.seed = seed
        self.personGen = PersonGenerator(self.seed)
        self.population = []

    def create(self):
        self.initial_pop()
        # self.add_spouses()
        # self.add_siblings()
        return self.population

    def initial_pop(self):
        for _ in range(FIRST_PASS_POP_SIZE):
            self.population.append(self.personGen.new(generation=1))

        # self.population.append(self.personGen.new(generation=5))

    # def add_siblings(self):
    #     sib_nums, sib_weights = load_weighted_csv(SIBLING_DATA_PATH)
    #     new_pop = []
    #     for person in self.population:
    #         numSibs = int(self.personGen.gen.weighted_choice(sib_nums, sib_weights))
    #         if numSibs:
    #             family = [person] + [
    #                 self.personGen.new_sibling(person) for _ in range(numSibs)
    #             ]
    #             for p in family:
    #                 p.siblings = [sib for sib in family if sib != p]
    #             new_pop.extend(family[1:])
    #         else:
    #             person.siblings = []
    #     self.population.extend(new_pop)

    def add_spouses(self):
        marriages, marriage_weights = load_weighted_csv(MARRIAGE_RATE_PATH)
        for person in self.population:
            if person.age >= MINIMUM_MARRIAGE_AGE:
                married_status = self.personGen.gen.weighted_choice(
                    marriages, marriage_weights
                )
                person.marital_status = married_status
                if (
                    married_status == "Married"
                    and person.sexual_orientation != "Asexual"
                ):
                    new_spouse = self.personGen.new_spouse(person)
                    person.spouse = new_spouse
                    self.population.append(new_spouse)

    def print_pop(self):
        for person in self.population:
            print(person)

    def csv_pop(self, filename=EXPORT_CSV_NAME):
        fields = [k for k in Person.__dict__.keys() if not k.startswith("__")]

        # writing to csv file
        with open(filename, "w") as csvfile:
            # creating a csv dict writer object
            writer = DictWriter(csvfile, fieldnames=fields)

            # writing headers (field names)
            writer.writeheader()

            # writing data rows
            for person in self.population:
                writer.writerow(
                    {k: v for k, v in person.__dict__.items() if k in fields}
                )
