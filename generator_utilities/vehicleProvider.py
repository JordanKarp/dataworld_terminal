from faker import Faker
from faker.providers import BaseProvider
from faker_vehicle import VehicleProvider
from pathlib import Path
from random import choices

from classes.vehicle import Vehicle
from generator_utilities.load_tools import load_weighted_csv

CAR_COLORS_PATH = Path("data/vehicle/vehicle_color_weights.csv")


class VehicleProvider(BaseProvider):
    gen = Faker()
    gen.add_provider(VehicleProvider)

    car_colors, car_color_weights = load_weighted_csv(CAR_COLORS_PATH)

    def car_color(self):
        return choices(self.car_colors, self.car_color_weights)[0]

    def personal_vehicle(self):
        vehicle_obj = self.gen.vehicle_object()
        year = vehicle_obj["Year"]
        make = vehicle_obj["Make"]
        model = vehicle_obj["Model"]
        type = vehicle_obj["Category"]
        # vin = self.gen.vin()
        license_plate_num = self.gen.license_plate()
        color = self.car_color()

        return Vehicle(
            year=year,
            make=make,
            model=model,
            type=type,
            color=color,
            # vin=vin,
            license_plate_num=license_plate_num,
        )
