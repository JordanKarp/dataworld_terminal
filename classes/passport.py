from dataclasses import dataclass


@dataclass
class Passport:
    number: str
    issue_date: str
    exp_date: str
    # restrictions: str

    def __getitem__(self, item):
        return getattr(self, item, "")
