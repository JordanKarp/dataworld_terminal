# from faker import Faker
from faker.providers import BaseProvider
from datetime import date
import calendar

GAME_YEAR = 2300
GAME_DATE = date(GAME_YEAR, 1, 1)
MIN_MARGIN = 1
MAX_MARGIN = 10


class DateProvider(BaseProvider):

    def today(self):
        return GAME_DATE

    def _random_month(self):
        return self.generator.random_int(1, 12)

    def _random_day(self, month_int, year=GAME_YEAR):
        days_in_month = calendar.monthrange(year, month_int)[1]
        return self.generator.random_int(1, days_in_month)

    def _random_year(self, start_year, end_year):
        return self.generator.random_int(start_year, end_year)

    def random_date_range(self, start_year, end_year=GAME_YEAR):
        y = self._random_year(start_year, end_year)
        m = self._random_month()
        d = self._random_day(m, y)
        return date(y, m, d)

    def random_date_margin(
        self,
        date=GAME_DATE,
        min_margin=MIN_MARGIN,
        max_margin=MAX_MARGIN,
    ):
        range1 = (date.year - max_margin, date.year - min_margin)
        range2 = (date.year + min_margin, date.year + max_margin)
        y1, y2 = self.generator.random_element([range1, range2])
        return self.random_date_range(y1, y2)
