from datetime import date
from dateutil.relativedelta import relativedelta
from string import ascii_uppercase
from pathlib import Path

from generator_providers.choicesProvider import ChoicesProvider
from generator_providers.dateProvider import DateProvider
from classes.passport import Passport
from classes.drivers_license import DriversLicense
from data.person.person_averages import YEARS_TIL_PASSPORT_EXP, YEARS_TIL_DL_EXP
from utilities.load_tools import load_weighted_csv

DL_RESTRICTIONS_PATH = Path("data/vehicle/dl_restrictions_weights.csv")


class DocumentProvider(ChoicesProvider, DateProvider):

    dl_rstr_list, dl_rstr_weights = load_weighted_csv(DL_RESTRICTIONS_PATH)

    def passport_num(self):
        return self.generator.bothify("?########", letters=ascii_uppercase)

    def passport_issue_date(self):
        # FIX
        # Passport issue date any date between gametoday and 10 years prior
        today = self.generator.today()
        year = (today - relativedelta(years=10)).year
        # return self.generator.random_date_range(date(year, 1, 1))
        return self.generator.date_between(date(year, 1, 1), today)

    def passport_exp_date(self, issue_date, passport_duration=YEARS_TIL_PASSPORT_EXP):
        return issue_date + relativedelta(years=passport_duration)

    def passport(self):
        issue = self.passport_issue_date()
        return Passport(
            self.passport_num(),
            issue,
            self.passport_exp_date(issue),
        )

    def dl_num(self):
        return self.generator.bothify("?##????#", letters=ascii_uppercase)

    def dl_issue_date(self):
        today = self.generator.today()
        year = (today - relativedelta(years=10)).year
        # return self.generator.random_date_range(date(year, today.month, today.day))
        return self.generator.date_between(date(year, 1, 1), today)

    def dl_exp_date(self, issue_date):
        return issue_date + relativedelta(years=YEARS_TIL_DL_EXP)

    def dl_restrictions(self):
        return self.weighted_choice(self.dl_rstr_list, self.dl_rstr_weights)

    def drivers_license(self):
        issue = self.dl_issue_date()
        return DriversLicense(
            self.dl_num(),
            issue,
            self.dl_exp_date(issue),
            self.dl_restrictions(),
        )
