from faker import Faker
from faker.providers import BaseProvider

from data.location.location_defaults import STATE_DICT
from classes.location import Location, LocationTypes, HomeTypes


class LocationProvider(BaseProvider):
    def home(self):
        state_abbr = self.generator.state_abbr()
        state = str(STATE_DICT[state_abbr])
        addr = self.generator.street_address()
        if "Suite" in addr:
            idx = addr.index("Suite")
            street_address_1 = addr[: idx - 1]
            street_address_2 = addr[idx:]
        elif "Apt" in addr:
            idx = addr.index("Apt")
            street_address_1 = addr[: idx - 1]
            street_address_2 = addr[idx:]
        else:
            street_address_1 = addr
            street_address_2 = ""
        city = self.generator.city()
        zipcode = self.generator.zipcode_in_state(state_abbr)
        country = "United States of America"
        loc_type = LocationTypes.HOME
        subtype = (
            HomeTypes.APARTMENT
            if "Suite" in street_address_2 or "Apt." in street_address_2
            else HomeTypes.SINGLE_FAMILY_HOME
        )

        return Location(
            street_address_1=street_address_1,
            street_address_2=street_address_2,
            city=city,
            state=state,
            zipcode=zipcode,
            country=country,
            loc_type=loc_type,
            subtype=subtype,
        )
