# from csv import DictWriter
from pathlib import Path

# from classes.person import Person
from generators.personGenerator import PersonGenerator
from utilities.load_tools import load_weighted_csv
from data.person.person_averages import TAKE_NAME_PERCENT

FIRST_PASS_POP_SIZE = 100
STARTING_GENERATION = 3


NUM_CHILDREN_PATH = Path("data/population/num_children_weights.csv")
MARRIAGE_RATE_PATH = Path("data/population/marrage_rates_weights.csv")

EXPORT_CSV_NAME = "results/TestPopulation.csv"


class PopulationGenerator:
    def __init__(self, seed=None, locations=[]) -> None:
        self.seed = seed
        self.locations = locations
        self.personGen = PersonGenerator(self.seed, locations)
        self.marriages, self.marriage_weights = load_weighted_csv(MARRIAGE_RATE_PATH)
        # self.population = []
        self.population = {}

    def create(self, init_pop=FIRST_PASS_POP_SIZE, start_gen=STARTING_GENERATION):
        self.initial_pop(init_pop, start_gen)
        for i in range(start_gen, -1, -1):
            self.add_friends(i)
            self.match_spouses(i)
            self.add_children(i)
        return self.population

    def initial_pop(self, number_people, gen):
        for _ in range(number_people):
            p = self.personGen.new(generation=gen)
            self.population[p.id] = p

    def add_children(self, generation):
        child_nums, child_nums_weights = load_weighted_csv(NUM_CHILDREN_PATH)
        new_pop = {}
        eligible_parents = [
            p
            for p in self.population.values()
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
                for parent in [person, person.spouse]:
                    parent.children = new_children_in_family

                for child in new_children_in_family:
                    child.siblings = [
                        sib for sib in new_children_in_family if sib != child
                    ]
                    new_pop[child.id] = child

                # new_pop.extend(new_children_in_family)

                # Shifted this up one level to give more chances for children
                if person.spouse in eligible_parents:
                    eligible_parents.remove(person.spouse)
        self.population.update(new_pop)

    def _marry_people(self, a, b):
        a.spouse = b
        b.spouse = a
        a.marital_status = "Married"
        b.marital_status = "Married"
        homes = [a.home, b.home]
        chosen_house = self.personGen.gen.random_element(homes)
        a.home = chosen_house
        b.home = chosen_house
        # add unchosen home back to available pool
        homes.remove(chosen_house)
        self.locations.append(homes[0])
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

    def add_friends(self, generation):
        eligible_people = [
            p
            for p in self.population.values()
            if p.generation == generation and p.is_alive
        ]
        num_close_friends = 3
        for p in eligible_people:
            for _ in range(num_close_friends):
                other = self.personGen.gen.random_element(eligible_people)
                if p != other:
                    p.friends.add(other)
                    other.friends.add(p)

    def match_spouses(self, generation):
        eligible_people = [
            p
            for p in self.population.values()
            if p.generation == generation and p.can_marry
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
