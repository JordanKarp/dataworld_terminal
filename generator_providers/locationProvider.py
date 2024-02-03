from faker import Faker
from faker.providers import BaseProvider

from data.location.location_defaults import STATE_DICT
from classes.location import Location, LocationTypes, HomeTypes


class LocationProvider(BaseProvider):
    gen = Faker()

    def home(self):
        state_abbr = self.generator.state_abbr()
        state = STATE_DICT[state_abbr]
        addr = self.generator.street_address()
        if "Suite" in addr:
            street_address_1 = addr[: addr.index("Suite") - 1]
            street_address_2 = addr[addr.index("Suite") :]
        elif "Apt" in addr:
            street_address_1 = addr[: addr.index("Apt") - 1]
            street_address_2 = addr[addr.index("Apt") :]
        else:
            street_address_1 = addr
            street_address_2 = ""
        city = self.generator.city()
        zipcode = self.generator.zipcode_in_state(state_abbr)
        type = LocationTypes.HOME
        subtype = (
            HomeTypes.APARTMENT
            if "Suite" in street_address_1 or "Apt." in street_address_1
            else HomeTypes.SINGLE_FAMILY_HOME
        )

        return Location(
            street_address_1, street_address_2, city, state, zipcode, type, subtype
        )
