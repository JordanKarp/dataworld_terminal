from dataclasses import dataclass
from enum import Enum, auto


class PhoneNumberTypes(Enum):
    CELL = auto()
    HOME = auto()
    WORK = auto()
    OTHER = auto()


@dataclass
class PhoneNumber:
    number: str = "defPhoneNumber"
    type: PhoneNumberTypes = PhoneNumberTypes.CELL

    def __getitem__(self, item):
        return getattr(self, item, "")

    def __repr__(self):
        return f"{self.type.name.title()}: {self.number}"
