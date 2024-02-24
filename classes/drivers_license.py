from dataclasses import dataclass


@dataclass
class DriversLicense:
    number: str
    issue_date: str
    exp_date: str
    restrictions: str

    def __repr__(self):
        return f"Driver's License: {self.number} - Exp: {self.exp_date:%b %Y}"

    def __getitem__(self, item):
        return getattr(self, item, "")
