from dataclasses import dataclass
from enum import Enum, auto


class EmailTypes(Enum):
    PERSONAL = auto()
    BUSINESS = auto()
    OTHER = auto()


@dataclass
class Email:
    address: str = "defEmail@test.com"
    type: EmailTypes = EmailTypes.PERSONAL

    @property
    def domain(self):
        if self.address and "@" in self.address:
            _, full_domain = self.address.split("@")
            if "." in full_domain:
                return full_domain.split(".")[0]
        return None

    def __getitem__(self, item):
        return getattr(self, item, "")

    def __repr__(self):
        return f"{self.type.name.title()}: {self.address}"
