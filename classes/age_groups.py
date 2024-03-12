from enum import Enum


class AgeGroups(Enum):
    INFANT = (0, 2)
    TODDLER = (2, 4)
    EARLY_CHILDHOOD = (4, 8)
    LATE_CHILDHOOD = (8, 11)
    EARLY_TEEN = (11, 15)
    LATE_TEEN = (15, 20)
    EARLY_YOUNG_ADULT = (20, 30)
    LATE_YOUNG_ADULT = (30, 40)
    MIDDLE_AGE = (40, 60)
    SENIOR = (60, 80)
    LATE_SENIOR = (80, 120)

    def __str__(self):
        return self.name.replace("_", " ").title()

    __repr__ = __str__

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value[1] < other.value[1]
        return NotImplemented

    @staticmethod
    def contains(age):
        try:
            return next(
                (
                    age_group
                    for age_group in AgeGroups
                    if age_group.value[0] <= age < age_group.value[1]
                ),
                None,
            )

        except (TypeError, ValueError, OverflowError):  # int conversion failed
            return None
