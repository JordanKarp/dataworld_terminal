from pathlib import Path

from classes.employee import EmployeeRole, EmployeeDemand
from classes.phone_number import PhoneNumber, PhoneNumberTypes

from generator_providers.choicesProvider import ChoicesProvider
from utilities.load_tools import load_weighted_csv, load_json

COMPANY_NAMES_PATH = Path("./data/company/company_names.json")
INDUSTRY_WEIGHTS_PATH = Path("./data/company/industry_weights.csv")
SUB_INDSTRY_WEIGHT_PATHS = {
    "AUTOMOTIVE": Path("./data/company/sub_auto_weights.csv"),
    "EDUCATION": Path("./data/company/sub_edu_weights.csv"),
    "ENTERTAINMENT": Path("./data/company/sub_ent_weights.csv"),
    "FINANCE": Path("./data/company/sub_fin_weights.csv"),
    "FOOD AND BEVERAGE": Path("./data/company/sub_food_weights.csv"),
    "HEALTHCARE": Path("./data/company/sub_health_weights.csv"),
    "HOSPITALITY": Path("./data/company/sub_hosp_weights.csv"),
    "RETAIL": Path("./data/company/sub_retail_weights.csv"),
    "TECHNOLOGY": Path("./data/company/sub_tech_weights.csv"),
    "TRANSPORTATION": Path("./data/company/sub_trans_weights.csv"),
}


class CompanyProvider(ChoicesProvider):
    names_dict = load_json(COMPANY_NAMES_PATH)

    def company_name(self, industry, sub_industry):
        ind_name_obj = self.names_dict[industry.upper()]
        first = self.generator.random_element(ind_name_obj["FIRST_OPTIONS"])
        sec = self.generator.random_element(ind_name_obj["SECOND_OPTIONS"])
        last = self.generator.random_element(ind_name_obj[sub_industry.upper()])
        if sec:
            return self.generator.random_element(
                [f"{first}{sec} {last}", f"{first} {sec} {last}"]
            )
        return f"{first} {last}"

    def industry(self):
        inds, ind_weights = load_weighted_csv(INDUSTRY_WEIGHTS_PATH)
        return self.weighted_choice(inds, ind_weights)

    def sub_industry(self, industry):
        path = SUB_INDSTRY_WEIGHT_PATHS[industry.upper()]
        sub_ind, sub_ind_weights = load_weighted_csv(path)
        return self.weighted_choice(sub_ind, sub_ind_weights)

    def website(self, company_name, domain_suff="com"):
        secure = "s" if self.generator.pybool() is True else ""
        name_str = "".join(company_name.split(" "))
        return f"kttp{secure}://www.{name_str.lower()}.{domain_suff}"

    def company_phone_number(self):
        return PhoneNumber(
            self.generator.numerify(text="(%#%) %##-####"), PhoneNumberTypes.WORK
        )

    def employee_structure(self, industry, sub_industry):
        # TODO create data for which industires have which structures (including roles and teams)
        # TODO load data
        # TODO Implement dad's aglo to make nesed employees

        owner = EmployeeDemand(EmployeeRole("Owner"), 1)
        mgrs = EmployeeDemand(EmployeeRole("Manager"), 2)
        emps = EmployeeDemand(EmployeeRole(), 5)

        return [owner, mgrs, emps]
