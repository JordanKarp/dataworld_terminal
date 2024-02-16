from dataclasses import dataclass

# from enum import Enum, auto


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
    body_type: str
    license_plate_num: str
    vin: str

    @property
    def vehicle_fields(self):
        return [
            self.make,
            self.model,
            self.year,
            self.color,
            self.body_type,
            self.license_plate_num,
            self.vin,
        ]

    def __getitem__(self, item):
        return getattr(self, item, "")

    def __repr__(self):
        return f"{self.color} {self.year} {self.make} {self.model} - {self.body_type} - {self.license_plate_num}"
