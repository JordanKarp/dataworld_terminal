import csv
from collections import defaultdict
from itertools import groupby
from pathlib import Path
from faker import Faker

from classes.data_source import DataSource
from classes.person import Person
from classes.company import Company

DATA_SOURCE_RESULTS_PATH = Path("results")


class DataSourceGenerator:
    def __init__(self, pop, comp, seed=None):
        self.gen = Faker()
        if seed:
            Faker.seed(seed)
        self.dataSources = []
        self.population = pop
        self.companies = comp

    def populate_sources(self):
        self.gen_master_people()
        self.gen_master_companies()
        self.gen_master_pets()
        self.gen_passports()
        self.gen_vehicle_registrations()
        self.gen_drivers_licenses()
        self.gen_birth_certificates()
        self.gen_death_certificates()
        self.gen_company_directories()
        self.gen_company_client_list()
        self.gen_industry_directories()

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

    def gen_master_people(self):
        fields = [
            attr
            for attr in Person.__dict__.keys()
            if not callable(getattr(Person, attr)) and not attr.startswith("__")
        ]
        self._generate_data_source("MasterPopulation", None, fields, self.population)

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
            "full_name",
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
            Path(f"results/companies/{company.company_name}").mkdir(
                parents=True, exist_ok=True
            )
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

    # def gen_location_directory(self):
    #     fields = [
    #         "home~city",
    #         "home~state",
    #     ]
    #     locations = defaultdict(set)
    #     for person in self.population.values():
    #         locations[person.home.state].add(person.home.city)

    def _get_additional_attr(self, person, cls, fld):
        return str(getattr(person, cls)[fld]) if getattr(person, cls) else " "

    def export(self):
        for source in self.dataSources:
            filename = DATA_SOURCE_RESULTS_PATH / f"{source.name}.csv"
            with open(filename, "w") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(source.fields)
                writer.writerows(source.data)
