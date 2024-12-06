from datetime import datetime, date, timedelta, time
from faker import Faker
from pathlib import Path

from classes.employee import Location

from generator_providers.choicesProvider import ChoicesProvider
from utilities.load_tools import load_json

TRANSACTION_YEARS = 1

# GROCERY_RATE = 52 / 365
# GROCERY_AMOUNT = 200
# FAV_STORE_RATE = 0.75
INDUSTRY_INFO = Path("./data/company/industry_info.json")

FAMILY_CALL_RATE = 0.15
FAMILY_TEXT_RATE = 0.3
FAMILY_MEDIA_RATE = 0.05
MIN_CALL_LENGTH = 1
MAX_CALL_LENGTH = 120
MIN_TEXT_CHAR = 1
MAX_TEXT_CHAR = 350
MIN_MEDIA_MB = 1
MAX_MEDIA_MB = 200


class TransactionsGenerator:
    def __init__(self, pop, comp, seed=None) -> None:
        self.gen = Faker()
        if seed:
            Faker.seed(seed)
        self.gen.add_provider(ChoicesProvider)
        self.industry_dict = load_json(INDUSTRY_INFO)
        self.pop = pop
        self.comp = comp
        self.data = {}

    def _return_all_dates(self, years):
        year_to_gen = datetime.now().year - years
        start_date = date(year_to_gen, 1, 1)
        end_date = datetime.now().date()
        return daterange(start_date, end_date)

    def _return_transactional_people(self):
        return [
            person
            for person in self.pop.values()
            if person.can_work and person.is_alive
        ]

    def _random_timedelta(self, min_minutes, max_minutes):
        return timedelta(minutes=self.gen.pyint(min_minutes, max_minutes))

    def generate_schedule(self, years=TRANSACTION_YEARS):
        for specific_date in self._return_all_dates(years):
            # print(specific_date)
            for person in self._return_transactional_people():
                schedule = []
                # Starting at home
                # start_time = datetime.strptime(specific_date, "%H:%M")
                start_time = datetime.combine(specific_date, datetime.min.time())
                sleep_hours = person.work_hours[0] - 1 if person.work_hours else 8
                end_time = (
                    start_time
                    + timedelta(hours=sleep_hours)
                    + self._random_timedelta(-30, 30)
                )
                schedule.append((person.home.short_addr, start_time, end_time))
                # schedule.append(("Home", start_time, end_time))

                # If it's a work day
                if specific_date.weekday() in person.work_days:
                    # Travel to work
                    start_time = end_time
                    end_time = start_time + self._random_timedelta(15, 45)
                    schedule.append(("Travel to Work", start_time, end_time))

                    # Working hours
                    start_time = end_time
                    end_time = start_time + timedelta(hours=len(person.work_hours))
                    schedule.append(("Work", start_time, end_time))

                # If person went anywhere today
                if len(schedule) > 1:
                    # Travel back home
                    start_time = end_time
                    end_time = start_time + self._random_timedelta(15, 45)
                    schedule.append(("Travel Home", start_time, end_time))

                    # End the day at home
                    start_time = end_time
                    schedule.append(
                        (
                            person.home.short_addr,
                            start_time,
                            end_time,
                        )
                    )

                print(schedule, sep="\n")

            #         schedule = [person.home]
            #         if specific_date.weekday() in person.work_days:
            #             schedule.append((person.employer, len(person.work_hours)))

            #         if len(schedule) > 1:
            #             schedule.append(person.home)

            #         for place, duration in schedule:
            #             self.travel_to(place, specific_date, duration, person)
            #         print(schedule)

    def generate(self, years=TRANSACTION_YEARS):
        for specific_date in self._return_all_dates(years):
            for person in self._return_transactional_people():
                for industry in self.industry_dict.keys():
                    if self.industry_dict[industry].get("FREQUENCY_RANGE"):
                        company, store = self.pick_company_from_industry(
                            industry, person
                        )
                        rate = person.favorites.get(industry, [0])[1]
                        if self.gen.percent_check(rate):
                            self.industry_purchases(
                                person, specific_date, industry, company
                            )
                        # if self.industry_dict[industry].get("CHECKIN"):
                        #     self.check_in_at_location(
                        #         person, specific_date, industry, store
                        #     )

                self.make_calls_and_texts(person, specific_date)
                # self.make_social_connect_post(person, specific_date)
                # Employee payday
                if person.is_working and specific_date.weekday() == 4:
                    self.purchase(person.employer, person, person.salary, specific_date)
        # travel

    def travel_to(self, place, date, duration, person):
        # Travel to location (GPS)
        # if CheckIn, check in
        # wait duration,
        # if purchase make purchase
        pass

    def pick_company_from_industry(self, industry, person):
        fav_store_rate = self.industry_dict[industry]["FAVORITE_STORE_RATE"]
        company = (
            self.comp[person.favorites[industry][0]]
            if self.gen.percent_check(fav_store_rate)
            else self.gen.random_element(
                [c for c in self.comp.values() if c.industry == industry]
            )
        )
        return company, self.gen.random_element(company.locations)

    def get_purchase_amount(self, industry):
        low, high = self.industry_dict[industry]["PURCHASE_RANGE"]
        return round(self.gen.pyfloat(min_value=low, max_value=high), 2)

    def get_random_workhour_datetime(self, industry, specific_date):
        open_hours, close_hours = self.industry_dict[industry]["HOURS"]
        return self._gen_random_datetime(specific_date, open_hours, close_hours)

    def purchase(self, buyer, seller, item_price, purchase_date):
        try:
            if not isinstance(purchase_date, datetime):
                purchase_date = datetime.combine(purchase_date, datetime.min.time())
            buyer.bank_account.withdraw(
                f"{seller.name} - Payment", item_price, purchase_date
            )
            seller.bank_account.deposit(
                f"Purchase by {buyer.name}", item_price, purchase_date
            )
        except Exception as e:
            print(f"error with {buyer} or {seller}")
            print(e)

    def industry_purchases(self, person, date, industry, store):
        amount = self.get_purchase_amount(industry)
        date_time = self.get_random_workhour_datetime(industry, date)
        self.purchase(person, store, amount, date_time)

    def _gen_random_datetime(self, given_date, start_hour, end_hour):
        # Convert opening and closing times to datetime objects on the given date
        opening_datetime = datetime.combine(given_date, time(start_hour))
        closing_datetime = datetime.combine(given_date, time(end_hour))

        # Generate a random number of seconds between opening and closing hours
        total_seconds = (closing_datetime - opening_datetime).seconds
        random_seconds = self.gen.pyint(0, total_seconds)
        return opening_datetime + timedelta(seconds=random_seconds)

    def make_calls_and_texts(self, person, specific_date):
        for family_member in person.list_of_family:
            if family_member.is_alive and family_member.phone_number:
                if self.gen.percent_check(FAMILY_CALL_RATE):
                    duration = self.gen.pyint(MIN_CALL_LENGTH, MAX_CALL_LENGTH)
                    date_time = self._gen_random_datetime(specific_date, 8, 22)

                    person.phone_number.make_call(
                        family_member.phone_number, date_time, f"{duration} minutes"
                    )
                if self.gen.percent_check(FAMILY_TEXT_RATE):
                    characters = self.gen.pyint(MIN_TEXT_CHAR, MAX_TEXT_CHAR)
                    date_time = self._gen_random_datetime(specific_date, 8, 22)

                    person.phone_number.send_text(
                        family_member.phone_number,
                        date_time,
                        f"{characters} characters",
                    )
                if self.gen.percent_check(FAMILY_MEDIA_RATE):
                    size = self.gen.pyint(MIN_MEDIA_MB, MAX_MEDIA_MB) / 10
                    date_time = self._gen_random_datetime(specific_date, 8, 22)

                    person.phone_number.send_media(
                        family_member.phone_number, date_time, f"{size} MB"
                    )

    def check_in_at_location(self, person, date, industry, store):
        date_time = self.get_random_workhour_datetime(industry, date)
        store.add_location_checkin(date_time, person)


def daterange(start_date: date, end_date: date):
    days = int((end_date - start_date).days)
    for n in range(days):
        yield start_date + timedelta(n)
