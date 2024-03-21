from dataclasses import dataclass


@dataclass
class Animal:
    name: str
    animal_type: str
    breed: str
    age: int
    gender: str

    def __getitem__(self, item):
        return getattr(self, item, "")
