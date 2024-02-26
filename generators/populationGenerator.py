from csv import DictWriter
from pathlib import Path


from classes.person import Person
from generators.personGenerator import PersonGenerator
from utilities.load_tools import load_weighted_csv

FIRST_PASS_POP_SIZE = 3
MINIMUM_MARRIAGE_AGE = 18
NUM_CHILDREN_PATH = Path("data/population/num_children_weights.csv")
MARRIAGE_RATE_PATH = Path("data/population/marrage_rates_weights.csv")

EXPORT_CSV_NAME = "results/TestPopulation.csv"


class PopulationGenerator:
    def __init__(self, seed=None) -> None:
        self.seed = seed
        self.personGen = PersonGenerator(self.seed)
        self.population = []

    def create(self):
        self.initial_pop()
        self.add_spouses()
        self.add_children()
        return self.population

    def initial_pop(self):
        for _ in range(FIRST_PASS_POP_SIZE):
            self.population.append(self.personGen.new(generation=2))

    def add_children(self):
        child_nums, child_nums_weights = load_weighted_csv(NUM_CHILDREN_PATH)
        new_pop = []
        eligible_parents = [p for p in self.population if p.marital_status == "Married"]
        for person in eligible_parents:
            num_children = int(
                self.personGen.gen.weighted_choice(child_nums, child_nums_weights)
            )
            if num_children:
                new_children_in_family = []
                for _ in range(num_children):
                    child = self.personGen.new_child(person, person.spouse)
                    new_children_in_family.append(child)

                for child in new_children_in_family:
                    child.siblings = [
                        sib for sib in new_children_in_family if sib != child
                    ]

                for parent in [person, person.spouse]:
                    parent.children = new_children_in_family

                new_pop.extend(new_children_in_family)

            if person.spouse in eligible_parents:
                eligible_parents.remove(person.spouse)
        self.population.extend(new_pop)

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
        new_spouses = []
        marriages, marriage_weights = load_weighted_csv(MARRIAGE_RATE_PATH)
        for person in self.population:
            if (
                person.age >= MINIMUM_MARRIAGE_AGE
                and person.marital_status != "Married"
                and person.sexual_orientation != "Asexual"
            ):
                person.marital_status = self.personGen.gen.weighted_choice(
                    marriages, marriage_weights
                )
                new_spouse = self.personGen.new_spouse(person)
                person.spouse = new_spouse
                new_spouses.append(new_spouse)
        self.population.extend(new_spouses)

    def __repr__(self):
        for person in self.population:
            print(person)

    # FIELDS IN ALPHABETICAL ORDER
    def csv_pop(self, filename=EXPORT_CSV_NAME):
        fields = [
            attr
            for attr in dir(Person)
            if not callable(getattr(Person, attr)) and not attr.startswith("__")
        ]

        with open(filename, "w") as csvfile:
            writer = DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            for person in self.population:
                writer.writerow({k: getattr(person, k) for k in fields})

    # def csv_pop(self, filename=EXPORT_CSV_NAME):
    #     fields = [k for k in Person.__dict__.keys() if not k.startswith("__")]

    #     # writing to csv file
    #     with open(filename, "w") as csvfile:
    #         # creating a csv dict writer object
    #         writer = DictWriter(csvfile, fieldnames=fields)

    #         # writing headers (field names)
    #         writer.writeheader()

    #         # writing data rows
    #         for person in self.population:
    #             writer.writerow(
    #                 {k: v for k, v in person.__dict__.items() if k in fields}
    #             )
