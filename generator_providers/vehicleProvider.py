from faker import Faker
from faker_vehicle import VehicleProvider
from pathlib import Path
import string
from dateutil.relativedelta import relativedelta

from data.person.person_averages import YEARS_TIL_DL_EXP

# from generator_utilities.random_tools import blank_or
from classes.vehicle import Vehicle
from classes.drivers_license import DriversLicense
from generator_utilities.load_tools import load_weighted_csv
from generator_providers.choicesProvider import ChoicesProvider

CAR_COLORS_PATH = Path("data/vehicle/vehicle_color_weights.csv")
DL_RESTRICTIONS_PATH = Path("data/vehicle/dl_restrictions_weights.csv")
ALL_CHAR_NUM = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


class CustomVehicleProvider(ChoicesProvider):

    gen = Faker()
    gen.add_provider(VehicleProvider)

    car_colors, car_color_weights = load_weighted_csv(CAR_COLORS_PATH)
    dl_restrictions_list, dl_restrictions_weights = load_weighted_csv(
        DL_RESTRICTIONS_PATH
    )

    def car_color(self):
        return self.weighted_choice(self.car_colors, self.car_color_weights)

    def dl_num(self):
        return self.generator.bothify("?##????#", letters=string.ascii_uppercase)

    def dl_issue_date(self):
        return self.generator.date_this_decade(after_today=False)

    def dl_restrictions(self):
        return self.weighted_choice(
            self.dl_restrictions_list, self.dl_restrictions_weights
        )

    def drivers_license(self):
        issue = self.dl_issue_date()
        return DriversLicense(
            self.dl_num(),
            self.dl_issue_date(),
            issue + relativedelta(years=YEARS_TIL_DL_EXP),
            self.dl_restrictions(),
        )

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
