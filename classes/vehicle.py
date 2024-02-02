from dataclasses import dataclass
from enum import Enum, auto


# class VehicleTypes(Enum):
#     CELL = auto()
#     HOME = auto()
#     WORK = auto()
#     OTHER = auto()


@dataclass
class Vehicle:
    make: str
    model: str
    year: int
    color: str
    license_plate_num: str
    type: str
    vin: str

    def __repr__(self):
        return f"{self.color} {self.year} {self.make} {self.model} - {self.type} - {self.license_plate_num}"
