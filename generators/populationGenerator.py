from csv import DictWriter
from pathlib import Path

from classes.person import Person
from generators.personGenerator import PersonGenerator
from utilities.load_tools import load_weighted_csv
from data.person.person_averages import TAKE_NAME_PERCENT

FIRST_PASS_POP_SIZE = 100
STARTING_GENERATION = 1
MINIMUM_MARRIAGE_AGE = 18

NUM_CHILDREN_PATH = Path("data/population/num_children_weights.csv")
MARRIAGE_RATE_PATH = Path("data/population/marrage_rates_weights.csv")

EXPORT_CSV_NAME = "results/TestPopulation.csv"


class PopulationGenerator:
    def __init__(self, seed=None) -> None:
        self.seed = seed
        self.personGen = PersonGenerator(self.seed)
        self.marriages, self.marriage_weights = load_weighted_csv(MARRIAGE_RATE_PATH)
        self.population = []

    def create(self, start_gen=STARTING_GENERATION):
        self.initial_pop(start_gen)
        for i in range(start_gen, -1, -1):
            self.match_spouses(i)
            self.add_children(i)
        return self.population

    def initial_pop(self, gen, number_people=FIRST_PASS_POP_SIZE):
        for _ in range(number_people):
            self.population.append(self.personGen.new(generation=gen))

    def add_children(self, generation):
        child_nums, child_nums_weights = load_weighted_csv(NUM_CHILDREN_PATH)
        new_pop = []
        eligible_parents = [
            p
            for p in self.population
            if p.marital_status == "Married" and p.generation == generation
        ]
        for person in eligible_parents:
            if num_children := int(
                self.personGen.gen.weighted_choice(child_nums, child_nums_weights)
            ):
                new_children_in_family = [
                    self.personGen.new_child(person, person.spouse)
                    for _ in range(num_children)
                ]
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

    def _marry_people(self, a, b):
        a.spouse = b
        b.spouse = a
        a.marital_status = "Married"
        b.marital_status = "Married"
        house = self.personGen.gen.random_element([a.home, b.home])
        a.home = house
        b.home = house
        if self.personGen.gen.percent_check(TAKE_NAME_PERCENT):
            if a.gender == "Male":
                b.maiden_name = str(b.last_name)
                b.last_name = a.last_name
            else:
                a.maiden_name = str(a.last_name)
                a.last_name = b.last_name

    def _is_eligible_match(self, person, match):
        return (
            match.gender == person.desired_gender
            and match is not person
            and match not in person.siblings
            and match.sexual_orientation == person.sexual_orientation
        )

    def match_spouses(self, generation):
        eligible_people = [
            p for p in self.population if p.generation == generation and p.can_marry
        ]

        for p in eligible_people:
            marital_status = self.personGen.gen.weighted_choice(
                self.marriages, self.marriage_weights
            )
            if marital_status == "Married":
                matches = [m for m in eligible_people if self._is_eligible_match(p, m)]
                spouse = self.personGen.gen.random_element(matches) if matches else None

                if spouse:
                    self._marry_people(p, spouse)
                    eligible_people.remove(spouse)
            if p in eligible_people:
                eligible_people.remove(p)

    def __repr__(self):
        return "\n".join(str(person) for person in self.population)

    # FIELDS IN ALPHABETICAL ORDER
    def population_to_csv(self, filename=EXPORT_CSV_NAME):
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
