from dataclasses import dataclass
from enum import Enum, auto


class EmailTypes(Enum):
    PERSONAL = auto()
    BUSINESS = auto()
    OTHER = auto()


@dataclass
class Email:
    address: str = "defEmail"
    type: EmailTypes = EmailTypes.PERSONAL

    def __repr__(self):
        return f"{self.type.name.title()}: {self.address}"
