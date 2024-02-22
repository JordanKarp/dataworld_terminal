from faker import Faker
from faker_vehicle import VehicleProvider
from pathlib import Path
from string import ascii_uppercase, digits
from dateutil.relativedelta import relativedelta

from data.person.person_averages import YEARS_TIL_DL_EXP

from classes.vehicle import Vehicle
from utilities.load_tools import load_weighted_csv
from generator_providers.choicesProvider import ChoicesProvider

CAR_COLORS_PATH = Path("data/vehicle/vehicle_color_weights.csv")
ALL_CHAR_NUM = ascii_uppercase + digits


class CustomVehicleProvider(ChoicesProvider):

    gen = Faker()
    gen.add_provider(VehicleProvider)

    car_colors, car_color_weights = load_weighted_csv(CAR_COLORS_PATH)

    def car_color(self):
        return self.weighted_choice(self.car_colors, self.car_color_weights)

    def vin(self):
        return self.gen.lexify(text="?" * 17, letters=ALL_CHAR_NUM)

    def personal_vehicle(self):
        vehicle_obj = self.gen.vehicle_object()
        year = vehicle_obj["Year"]
        make = vehicle_obj["Make"]
        model = vehicle_obj["Model"]
        body_type = vehicle_obj["Category"]
        vin = self.vin()
        license_plate_num = self.gen.license_plate()
        color = self.car_color()

        return Vehicle(
            year=year,
            make=make,
            model=model,
            body_type=body_type,
            color=color,
            vin=vin,
            license_plate_num=license_plate_num,
        )
