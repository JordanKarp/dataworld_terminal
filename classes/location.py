from dataclasses import dataclass
from enum import Enum, auto

from data.location.location_defaults import STATE_ABBR_DICT


class LocationTypes(Enum):
    HOME = auto()
    BUSINESS = auto()
    OTHER = auto()


class HomeTypes(Enum):
    APARTMENT = auto()
    SINGLE_FAMILY_HOME = auto()
    OTHER = auto()


@dataclass
class Location:
    street_address_1: str = "1 default st."
    street_address_2: str = ""
    city: str = "DefaultCity"
    state: str = "DefaultState"
    zipcode: str = "00000"
    type: LocationTypes = LocationTypes.OTHER
    subtype: HomeTypes = HomeTypes.OTHER

    def state_abbr(self):
        return STATE_ABBR_DICT[self.state]
