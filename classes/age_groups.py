from enum import Enum


class AgeGroups(Enum):
    INFANT = range(2)
    TODDLER = range(2, 4)
    EARLY_CHILDHOOD = range(4, 8)
    LATE_CHILDHOOD = range(8, 11)
    EARLY_TEEN = range(11, 15)
    LATE_TEEN = range(15, 20)
    EARLY_YOUNG_ADULT = range(20, 30)
    LATE_YOUNG_ADULT = range(30, 40)
    MIDDLE_AGE = range(40, 60)
    SENIOR = range(60, 80)
    LATE_SENIOR = range(80, 120)
