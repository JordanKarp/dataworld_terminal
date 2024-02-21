from enum import Enum, auto


class Industries(Enum):
    AUTOMOTIVE = auto()
    EDUCATION = auto()
    ENTERTAINMENT = auto()
    FINANCE = auto()
    FOOD_AND_BEVERAGE = auto()
    HEALTHCARE = auto()
    HOSPITALITY = auto()
    RETAIL = auto()
    TECHNOLOGY = auto()
    TRANSPORTATION = auto()

    def __repr__(self):
        return self.name.replace("_", " ").title()


# class SubIndustry(Enum):
#     pass

# class AutomotiveSubIndustry(SubIndustry):
