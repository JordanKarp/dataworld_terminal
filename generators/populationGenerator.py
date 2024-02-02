from pathlib import Path
from random import choices

from generators.personGenerator import PersonGenerator
from generator_utilities.load_tools import load_weighted_csv

FIRST_PASS_POP_SIZE = 1
SIBLING_DATA_PATH = Path("data/population/num_children_weights.csv")


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

        self.population.extend(new_pop)

    def add_spouses(self):
        pass

    def print_pop(self):
        for person in self.population:
            print(person)
