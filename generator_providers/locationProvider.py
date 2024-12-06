from faker.providers import BaseProvider
from data.location.location_defaults import STATE_DICT
from classes.location import Location, LocationTypes, HomeTypes, BusinessTypes


class LocationProvider(BaseProvider):

    def _parse_address(self, addr):
        num, addr_name = addr.split(" ", 1)
        street_num = int(num)
        for keyword in ["Suite", "Apt"]:
            before, separator, after = addr_name.partition(keyword)
            if separator:
                return f"{street_num} {before.strip()}", f"{separator}{after}"
        return f"{street_num} {addr_name.strip()}", ""

    def _create_location(
        self, street_address_1, street_address_2, city, state_abbr, loc_type, subtype
    ):
        state = str(STATE_DICT[state_abbr])
        zipcode = self.generator.zipcode_in_state(state_abbr)
        country = "United States of America"
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

    def home(self):
        state_abbr = self.generator.state_abbr()
        state_abbr = "NJ"
        addr = self.generator.street_address()
        street_address_1, street_address_2 = self._parse_address(addr)
        city = self.generator.city()
        loc_type = LocationTypes.HOME
        subtype = (
            HomeTypes.APARTMENT
            if "Suite" in street_address_2 or "Apt." in street_address_2
            else HomeTypes.SINGLE_FAMILY_HOME
        )
        return self._create_location(
            street_address_1, street_address_2, city, state_abbr, loc_type, subtype
        )

    def company_hq(self):
        state_abbr = self.generator.state_abbr()
        addr = self.generator.street_address()
        street_address_1, _ = self._parse_address(addr)
        city = self.generator.city()
        loc_type = LocationTypes.BUSINESS
        subtype = BusinessTypes.HQ
        return self._create_location(
            street_address_1, "", city, state_abbr, loc_type, subtype
        )
