from dataclasses import dataclass, field
from datetime import datetime
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


class BusinessTypes(Enum):
    HQ = auto()
    OTHER = auto()


@dataclass
class LocationCheckin:
    date: datetime
    name: str


@dataclass
class Location:
    street_address_1: str = "1 Default st."
    street_address_2: str = ""
    city: str = "DefaultCity"
    state: str = "DefaultState"
    zipcode: str = "00000"
    country: str = "United States of America"
    building_type: str = "Universal"
    value: str = "0"
    lot_size: str = "0"
    checkin_log: list[LocationCheckin] = field(default_factory=list, repr=True)

    @property
    def citystate(self):
        return f"{self.city}, {self.state}"
        # return f"{self.city}, {self.state_abbr}"

    @property
    def address(self):
        address_2 = f" - {self.street_address_2}" if self.street_address_2 else ""
        return f"{self.street_address_1}{address_2}, {self.city}, {self.state} - {self.zipcode}"
        # return f"{self.street_address_1}{address_2}, {self.city}, {self.state_abbr} - {self.zipcode}"

    @property
    def short_addr(self):
        if self.street_address_2:
            return f"{self.street_address_1} - {self.street_address_2}"
        else:
            return self.street_address_1

    def __getitem__(self, item):
        return getattr(self, item, "")

    def __repr__(self):
        return f"{self.building_type} (val:{self.value}/size:{self.lot_size}): {self.address}"

    def add_location_checkin(self, date, name):
        checkin = LocationCheckin(date, name)
        self.checkin_log.append(checkin)
