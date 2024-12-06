import contextlib
from collections import defaultdict
import csv
from itertools import groupby
from pathlib import Path
from faker import Faker
import shutil
from tabulate import tabulate


# from pprint import pprint as print
import json


from classes.data_source import DataSource
from classes.person import Person
from classes.company import Company
from classes.website import Website
from generator_providers.personFilters import get_pop_with_siblings

DATA_SOURCE_RESULTS_PATH = Path("results")
WEBSITE_RESULTS_PATH = Path("results/web")

tabulate.PRESERVE_WHITESPACE = True


class DataSourceGenerator:
    def __init__(self, pop, comp, locs, missions=None, seed=None):
        self.gen = Faker()
        if seed:
            Faker.seed(seed)
        self.dataSources = []
        self.websites = []
        self.population = pop
        self.companies = comp
        self.locations = locs
        self.missions = missions

    def populate_sources(self):

        # self.gen_location_directory()
        self._create_folder_structure()
        self.gen_master_people()
        self.gen_master_companies()

        # self.gen_master_pets()
        # self.gen_passports()
        # self.gen_vehicle_registrations()
        # self.gen_drivers_licenses()
        # self.gen_birth_certificates()
        # self.gen_death_certificates()
        # self.gen_company_directories()
        # self.gen_company_client_list()
        # self.gen_industry_directories()
        # self.gen_sibling_list()

        self.gen_company_bank_account()
        self.gen_person_bank_account()
        self.gen_person_phone_records()
        # self.gen_intro_website()
        # self.gen_tool_tutorial()
        # self.gen_company_homepages()
        # self.gen_company_aboutpages()
        # self.gen_company_contactpages()
        # self.gen_person_lookup()

        # self.gen_missions()

    def _create_folder_structure(self):
        with contextlib.suppress(Exception):
            # Remove previous companies
            shutil.rmtree(Path("results/companies/"))
            shutil.rmtree(Path("results/people/"))
            # Generate basic companies folder
            Path("results/companies").mkdir(parents=True, exist_ok=True)
            Path("results/people").mkdir(parents=True, exist_ok=True)
        for company in self.companies.values():
            # Make folder for each company
            Path(f"results/companies/{company.name}").mkdir(parents=True, exist_ok=True)
        for person in self.population.values():
            # Make folder for each company
            Path(f"results/people/{person.name}").mkdir(parents=True, exist_ok=True)

    def _check_requirements(self, obj, requirements=None):
        if requirements:
            for req in requirements:
                if not hasattr(obj, req) or getattr(obj, req) in [None, " ", ""]:
                    return False
        return True

    def _generate_data_source(
        self, name, requirements, fields, population_group, additional_attr_getter=None
    ):
        data = []
        group_list = (
            population_group.values()
            if isinstance(population_group, dict)
            else population_group
        )
        for obj in group_list:
            if not self._check_requirements(obj, requirements):
                continue
            obj_data = []
            for field in fields:
                if "~" in field:
                    cls, fld = field.split("~")
                    attr_value = (
                        additional_attr_getter(obj, cls, fld)
                        if additional_attr_getter
                        else " "
                    )
                else:
                    attr_value = getattr(obj, field, " ")
                obj_data.append(attr_value)
            data.append(obj_data)
        self.dataSources.append(DataSource(name, fields, data))

    def gen_intro_website(self):
        self.websites.append(
            Website(
                slug="index",
                url="www.dataworld.com/intro",
                title="Dataworld Introduction",
                searchable=True,
                html=(
                    "<font size='6'>Welcome to Dataworld!</font><br><hr><br>"
                    "Welcome to Dataworld, where debts become opportunities and challenges lead to rewards.<br><br>"
                    "In a world burdened by towering debts, you've made a bold decision—to sell your debt of <b>$35,273,398.42</b> to Dataworld. In exchange for shouldering your financial burdens, Dataworld offers a unique proposition: become a Data Solver! (Your new debt has amounted to <b>$143,993.42</b> with monthly fees of <b>$2,2038.32</b>. You can see a full breakdown of your debt using one of the links below.)<br><br>"
                    "As a Data Solver, you'll embark on a journey of problem-solving and data mastery. Your mission? To tackle a variety of tasks, each presenting its own set of challenges and rewards. From unraveling complex puzzles to analyzing intricate datasets, the path to financial freedom lies in your ability to thrive in the realm of data.<br><br>"
                    "Remember, your progress is measured by your performance. Complete missions to climb the ranks, unlocking greater opportunities and rewards along the way. The choice of mission, difficulty, and payout is yours to make—forge your path to success in the world of Data Solvers.<br><br>"
                    "So, are you ready to embrace the challenge and rewrite your financial destiny? Step into Dataworld and let the journey begin.<br><br>"
                    "Helpful getting started links:<br>"
                    " - <a href='dataworld~guide'>Beginner's Guide to Data Solving</a><br>"
                    " - <a href='dataworld~debt'>Debt Breakdown</a><br>"
                    " - <a href='dataworld~tool'>Tool Tutorial</a><br>"
                    " - <a href='dataworld~sources'>Acquiring More Data Soures</a><br>"
                    "<br>"
                    "Best of luck to you and happy solving!<br>"
                    "Dataworld"
                ),
            )
        )

    def gen_tool_tutorial(self):
        self.websites.append(
            Website(
                slug="dataworld~tool",
                url="www.dataworld.com/tutorial/tools",
                title="Dataworld Tools",
                searchable=True,
                html=(
                    "<font size='6'>Tool Overview</font><br><hr><br>"
                    "<b>Web Browser</b>: your main source of information.<br>"
                    "Use the search bar to navigate through publically available websites. Not every website can be found through the search however.<br>"
                    "In some cases, you'll need to know the exact url to access, some websites will have even further authetication required.<br>"
                    " - <a href='peoplefinder'>PeopleFinder</a> - A handy lookup for the name, address and phone number of the head of household. Some houses may be unlisted.<br>"
                    " - <a href='companylookup'>CompanyLookup</a> - Look up valuable information on publically traded companies. More in depth information can be revealed with higher memebership tiers.<br>"
                    " - <a href='dataworld'>Dataworld homepage</a> -  Your main homepage for finding dataworld news, updates and currents status. You can take on new missions here, as well as go back through tutorials.<br>"
                    " - <a href='socialmedia'>Social Media</a> - TODO<br>"
                    " - ...<br>"
                    "More tools will be listed here as they are discovered"
                ),
            )
        )

    def gen_person_lookup(self):
        pop = sorted(
            self.population.values(),
            key=lambda p: (p["last_name"], p["first_name"], p["middle_name"]),
        )

        html = f"<b>{'Name'.center(17)} {'Phone Number'.center(15)}    {'Address'.center(25)}</b><br>"
        html += "".join(
            f"<b>{p.name.ljust(17)}</b> {str(p.phone_number).center(15)}   {str(p.home.address).center(25)}<br>"
            for p in pop
            if p.home and p.phone_number and p.is_alive
        )
        site = Website(
            slug="peoplesearch",
            url="www.peoplesearch.com",
            title="People Search",
            html=html,
            searchable=True,
        )
        self.websites.append(site)

    def gen_company_homepages(self):
        for c in self.companies.values():
            site = Website(
                slug=c.slug,
                url=c.website_url,
                title=c.company_name,
                html=c.homepage_html,
                searchable=True,
            )
            self.websites.append(site)

    def gen_company_aboutpages(self):
        for c in self.companies.values():
            site = Website(
                slug=f"{c.slug}~about",
                url=f"{c.website_url}/about",
                title=f"{c.company_name}: About",
                html=c.about_html,
                searchable=False,
            )
            self.websites.append(site)

    def gen_company_contactpages(self):
        for c in self.companies.values():
            site = Website(
                slug=f"{c.slug}~contact",
                url=f"{c.website_url}/contact",
                title=f"{c.company_name}: Contact Us",
                html=c.contact_html,
                searchable=False,
            )
            self.websites.append(site)

    def gen_master_people(self):
        fields = [
            attr
            for attr in Person.__dict__.keys()
            if not callable(getattr(Person, attr)) and not attr.startswith("__")
        ]
        self._generate_data_source("MasterPopulation", None, fields, self.population)

    def gen_sibling_list(self):
        fields = [
            attr
            for attr in Person.__dict__.keys()
            if not callable(getattr(Person, attr)) and not attr.startswith("__")
        ]
        # print(self.population)
        pop = get_pop_with_siblings(self.population.values())
        self._generate_data_source("SiblingList", None, fields, pop)

    def gen_master_companies(self):
        fields = [
            attr
            for attr in Company.__dict__.keys()
            if not callable(getattr(Company, attr)) and not attr.startswith("__")
        ]
        self._generate_data_source("MasterCompanies", None, fields, self.companies)

    def gen_master_pets(self):
        fields = [
            "pet~name",
            "last_name",
            "pet~animal_type",
            "pet~breed",
            "pet~age",
            "pet~gender",
            "name",
        ]
        self._generate_data_source(
            "MasterPets",
            ["pet"],
            fields,
            self.population,
            self._get_additional_attr,
        )

    def gen_drivers_licenses(self):
        fields = [
            "full_name",
            "drivers_license~number",
            "drivers_license~issue_date",
            "drivers_license~exp_date",
            "drivers_license~restrictions",
            "home~state",
            "height",
            "format_height",
            "format_weight",
        ]
        self._generate_data_source(
            "DriversLicenses",
            ["drivers_license"],
            fields,
            self.population,
            self._get_additional_attr,
        )

    def gen_vehicle_registrations(self):
        fields = [
            "full_name",
            "vehicle~make",
            "vehicle~model",
            "vehicle~year",
            "vehicle~color",
            "vehicle~body_type",
            "vehicle~license_plate_num",
            "vehicle~vin",
        ]
        self._generate_data_source(
            "VehicleRegistrations",
            ["vehicle"],
            fields,
            self.population,
            self._get_additional_attr,
        )

    def gen_passports(self):
        fields = [
            "full_name",
            "home~address",
            "gender_abbr",
            "format_height",
            "format_weight",
            "eye_color",
            "passport~number",
            "passport~issue_date",
            "passport~exp_date",
            "home~country",
        ]
        self._generate_data_source(
            "Passports",
            ["passport"],
            fields,
            self.population,
            self._get_additional_attr,
        )

    def gen_birth_certificates(self):
        fields = [
            "gender",
            "date_of_birth",
            "time_of_birth",
            "first_name",
            "middle_name",
            "last_name",
            "parents",
        ]
        self._generate_data_source(
            "BirthCertificates",
            ["date_of_birth"],
            fields,
            self.population,
            self._get_additional_attr,
        )

    def gen_death_certificates(self):
        fields = [
            "full_name",
            "gender",
            "ssn",
            "years_lived",
            "age",
            "date_of_death",
            "marital_status",
        ]
        self._generate_data_source(
            "DeathCertificates",
            ["date_of_death"],
            fields,
            self.population,
            self._get_additional_attr,
        )

    def gen_company_directories(self):
        fields = ["full_name", "employer", "role", "email", "phone_number"]
        for company in self.companies.values():
            employees = {
                p.person.id: p.person
                for p in company.employee_structure
                if p.person is not None
            }
            comp_path = Path(
                f"companies/{company.company_name}/{company.abbreviation}_Directory"
            )
            self._generate_data_source(
                comp_path,
                None,
                fields,
                employees,
                self._get_additional_attr,
            )

    def gen_company_client_list(self):
        fields = ["full_name"]
        for company in self.companies.values():
            clients = {p.id: p for p in company.clients}

            comp_path = Path(
                f"companies/{company.company_name}/{company.abbreviation}_Clients"
            )
            self._generate_data_source(
                comp_path,
                None,
                fields,
                clients,
                self._get_additional_attr,
            )

    def gen_company_bank_account(self):
        fields = ["date", "description", "amount", "balance"]
        for company in self.companies.values():
            transactions = company.bank_account.transactions
            # transactions.sort(key=lambda x: x.date, reverse=False)
            comp_path = Path(
                f"companies/{company.name}/{company.name}_bank_transactions"
            )
            self._generate_data_source(
                comp_path,
                None,
                fields,
                transactions,
                self._get_additional_attr,
            )

    def gen_person_bank_account(self):
        fields = ["date", "description", "amount", "balance"]
        for person in self.population.values():
            if person.bank_account:
                transactions = person.bank_account.transactions
                transactions.sort(key=lambda x: x.date, reverse=False)
                comp_path = Path(
                    f"people/{person.name}/{person.name}_bank_transactions"
                )
                self._generate_data_source(
                    comp_path,
                    None,
                    fields,
                    transactions,
                    self._get_additional_attr,
                )

    def gen_person_phone_records(self):
        fields = ["date", "to", "from_", "size", "type_"]
        for person in self.population.values():
            if person.phone_number:
                events = person.phone_number.log
                events.sort(key=lambda x: x.date, reverse=False)
                comp_path = Path(f"people/{person.name}/{person.name}_phone_log")
                self._generate_data_source(
                    comp_path,
                    None,
                    fields,
                    events,
                    self._get_additional_attr,
                )

    def gen_industry_directories(self):
        fields = [
            "id",
            "company_name",
            "website",
            "industry",
            "sub_industry",
            "founded",
            "client_scope",
            "hq",
            "market_share",
            "abbreviation",
        ]
        sorted_companies = sorted(self.companies.values(), key=lambda c: c["industry"])
        for industry, industry_group in groupby(
            sorted_companies, key=lambda c: c["industry"]
        ):
            self._generate_data_source(
                f"industries/{industry}_Directory",
                None,
                fields,
                industry_group,
                self._get_additional_attr,
            )

    def gen_location_directory(self):
        # fields = [
        #     "citystate",
        #     "city",
        #     "num",
        # ]
        locations = defaultdict(lambda: 0)
        for person in self.population.values():
            if person.home:
                locations[person.home.citystate] += 1
        # print(max(locations.values()))

    def gen_missions(self):
        fields = [
            "id",
            "title",
            "text",
            "_solution",
        ]
        self._generate_data_source("MissionList", None, fields, self.missions)

        # for mission in self.missions.values():
        #     print(mission)

    def _get_additional_attr(self, person, cls, fld):
        return str(getattr(person, cls)[fld]) if getattr(person, cls) else " "

    def export(self):

        web_data = {"webdata": {}}
        for site in self.websites:
            web_data["webdata"][site.slug] = {
                "id_slug": site.slug,
                "url": site.url,
                "title": site.title,
                "searchable": site.searchable,
                "html": site.html,
            }
        with open(
            DATA_SOURCE_RESULTS_PATH / "web_data.json", "w", encoding="utf-8"
        ) as f:
            json.dump(web_data, f, indent=4)

        for source in self.dataSources:
            filename = DATA_SOURCE_RESULTS_PATH / f"{source.name}.csv"
            with open(filename, "w") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(source.fields)
                writer.writerows(source.data)

    # def htmlify(self, string):

    #     val = string.replace("\n", "<br>\n")

    def print_table(self):
        for source in self.dataSources:
            tbl = source.data
            newtbl = tabulate(tbl, headers=source.fields, tablefmt="github")
            newtbl = newtbl.replace("\n", "<br>\n")
            newtbl += "<br>"
            print(newtbl)
            # for line in newtbl:
            #     line.replace("\r\n", "<br>\n")
            #     print(line)
