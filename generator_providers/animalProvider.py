from pathlib import Path

from classes.animal import Animal

from generator_providers.choicesProvider import ChoicesProvider
from utilities.load_tools import load_weighted_csv, load_json

PET_OWNERSHIP_PERCENT = 0.50
ANIMAL_DATA_PATH = Path("./data/animal/master_pets.json")
PET_WEIGHTS_PATH = Path("./data/animal/pet_weights.csv")


class AnimalProvider(ChoicesProvider):
    pet_data = load_json(ANIMAL_DATA_PATH)
    pets, pet_weights = load_weighted_csv(PET_WEIGHTS_PATH)

    def new_pet(self, **kwargs):
        animal_type = kwargs.get("pet_type", self.pet_type())
        breed = kwargs.get("pet_breed", self.breed(animal_type))
        name = kwargs.get("pet_name", self.pet_name(animal_type))
        age = kwargs.get("pet_age", self.pet_age(animal_type))
        gender = kwargs.get("pet_gender", self.pet_gender())
        return self.blank_or(
            Animal(name, animal_type, breed, age, gender), PET_OWNERSHIP_PERCENT
        )

    def breed(self, animal_type):
        options = self.pet_data["animals"][animal_type]["breeds"]
        return self.random_element(options)

    def pet_type(self):
        return self.weighted_choice(self.pets, self.pet_weights)

    def pet_name(self, animal_type):
        options = self.pet_data["animals"][animal_type]["names"]
        return self.random_element(options)

    def pet_age(self, animal_type):
        max_age = self.pet_data["animals"][animal_type]["max_age"]
        return self.generator.pyint(0, max_age)

    def pet_gender(self):
        return self.random_element(["Male", "Female"])
