from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


from data.location.location_defaults import STATE_ABBR_DICT


class LocationTypes(Enum):
    HOME = auto()
    BUSINESS = auto()
    OTHER = auto()


class HomeTypes(Enum):
    APARTMENT = auto()
    SINGLE_FAMILY_HOME = auto()
    OTHER = auto()


class BusinessTypes(Enum):
    HQ = auto()
    OTHER = auto()


@dataclass
class Location:
    street_address_1: str = "1 Default st."
    street_address_2: str = ""
    city: str = "DefaultCity"
    state: str = "DefaultState"
    zipcode: str = "00000"
    country: str = "United States of America"
    loc_type: LocationTypes = LocationTypes.OTHER
    subtype: Optional[Enum] = None

    @property
    def state_abbr(self):
        return STATE_ABBR_DICT[self.state]

    @property
    def address(self):
        if self.street_address_2:
            return f"{self.street_address_1} - {self.street_address_2}, {self.city}, {self.state_abbr} - {self.zipcode}"
        else:
            return f"{self.street_address_1}, {self.city}, {self.state_abbr} - {self.zipcode}"

    def __getitem__(self, item):
        return getattr(self, item, "")

    def __repr__(self):
        return f"{self.loc_type.name.title()}: {self.address}"
