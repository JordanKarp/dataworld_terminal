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

    def passport_issue_date(self, date_of_death=None):
        # FIX
        # Passport issue date any date between gametoday and 10 years prior
        upper_date = date_of_death or self.generator.today()
        year = (upper_date - relativedelta(years=10)).year
        return self.generator.date_between(date(year, 1, 1), upper_date)

    def passport_exp_date(self, issue_date, passport_duration=YEARS_TIL_PASSPORT_EXP):
        return issue_date + relativedelta(years=passport_duration)

    def passport(self, date_of_death=None):
        issue = self.passport_issue_date(date_of_death)
        return Passport(
            self.passport_num(),
            issue,
            self.passport_exp_date(issue),
        )

    def dl_num(self):
        return self.generator.bothify("?##????#", letters=ascii_uppercase)

    def dl_issue_date(self, date_of_death=None):
        upper_date = date_of_death or self.generator.today()
        year = (upper_date - relativedelta(years=10)).year
        return self.generator.date_between(date(year, 1, 1), upper_date)

    def dl_exp_date(self, issue_date):
        return issue_date + relativedelta(years=YEARS_TIL_DL_EXP)

    def dl_restrictions(self):
        return self.weighted_choice(self.dl_rstr_list, self.dl_rstr_weights)

    def drivers_license(self, date_of_death=None):
        issue = self.dl_issue_date(date_of_death)
        return DriversLicense(
            self.dl_num(),
            issue,
            self.dl_exp_date(issue),
            self.dl_restrictions(),
        )
