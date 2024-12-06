from pathlib import Path
import json

from classes.employee import EmployeeRole
from classes.phone_number import Phone

from generator_providers.choicesProvider import ChoicesProvider
from generator_providers.dateProvider import DateProvider
from utilities.load_tools import load_weighted_csv, load_json, load_csv
from utilities.word_tools import (
    remove_last_vowel,
    remove_last_letter,
    capitalize_first,
    lower_first,
    BIZ_ADJS,
    INSP_VERBS,
    INSP_GRUNDS,
    BIZ_ADVBS,
)

COMPANY_NAMES_PATH = Path("./data/company/company_names.json")
# COMPANY_FOUNDED_PATH = Path("./data/company/company_ages_weights.csv")
# INDUSTRY_WEIGHTS_PATH = Path("./data/company/industry_weights.csv")
# SUB_INDSTRY_WEIGHT_PATHS = {
#     "AUTOMOTIVE": Path("./data/company/sub_auto_weights.csv"),
#     "EDUCATION": Path("./data/company/sub_edu_weights.csv"),
#     "ENTERTAINMENT": Path("./data/company/sub_ent_weights.csv"),
#     "FINANCE": Path("./data/company/sub_fin_weights.csv"),
#     "FOOD AND BEVERAGE": Path("./data/company/sub_food_weights.csv"),
#     "HEALTHCARE": Path("./data/company/sub_health_weights.csv"),
#     "HOSPITALITY": Path("./data/company/sub_hosp_weights.csv"),
#     "RETAIL": Path("./data/company/sub_retail_weights.csv"),
#     "TECHNOLOGY": Path("./data/company/sub_tech_weights.csv"),
#     "TRANSPORTATION": Path("./data/company/sub_trans_weights.csv"),
# }

INDUSTRY_INFO = Path("./data/company/industry_info.json")


class CompanyProvider(ChoicesProvider, DateProvider):
    # names_dict = load_json(COMPANY_NAMES_PATH)
    # founded_ranges, founded_weights = load_weighted_csv(COMPANY_FOUNDED_PATH)
    industry_dict = load_json(INDUSTRY_INFO)

    # def company_name(self, industry, sub_industry):
    #     ind_name_obj = self.names_dict[industry.upper()]
    #     first = self.generator.random_element(ind_name_obj["FIRST_OPTIONS"])
    #     sec = self.generator.random_element(ind_name_obj["SECOND_OPTIONS"])
    #     last = self.generator.random_element(ind_name_obj[sub_industry.upper()])
    #     if sec:
    #         return self.generator.random_element(
    #             [f"{first}{sec} {last}", f"{first} {sec} {last}"]
    #         )
    #     return f"{first} {last}"

    def name(self, industry):
        word = self.generator.random_element(
            self.industry_dict[industry]["NOUNS"].split(", ")
            + self.industry_dict[industry]["VERBS"].split(", ")
            + self.industry_dict[industry]["ADJECTIVES"].split(", ")
        )
        name_options = [
            f"{word}r",
            f"{word}It",
            f"{word}ly",
            f"{word}ify",
            f"{word}Hub",
            f"{word}y",
            f"{word}me",
            f"you{word}",
            f"{word}n",
            f"{word}str",
            remove_last_vowel(word),
            f"{word}Now",
            f"{word}Link",
            f"{word}in",
            f"{word}able",
            f"Smart{word}",
            f"We{word}",
            word + word,
        ]
        return self.generator.random_element(name_options)

    def slogan(self, industry):
        noun = self.generator.random_element(
            (self.industry_dict[industry]["NOUNS"].split(", "))
        )
        verb = self.generator.random_element(
            self.industry_dict[industry]["VERBS"].split(", ")
        )
        adjective = self.generator.random_element(
            self.industry_dict[industry]["ADJECTIVES"].split(", ")
        )
        biz_adj = self.generator.random_element(BIZ_ADJS)
        # biz_advb = self.generator.random_element(BIZ_ADVBS)
        insp_verb = self.generator.random_element(INSP_VERBS)
        insps_gerund = self.generator.random_element(INSP_GRUNDS)
        slogan_options = [
            f"Like no other {noun}.",
            f"{verb} like never before.",
            f"World's most {lower_first(biz_adj)} {noun}.",
            f"World's most {lower_first(adjective)} {noun}.",
            f"The {biz_adj} way to {verb}.",
            f"The {biz_adj} {noun}.",
            f"The {adjective} {noun}.",
            f"{capitalize_first(verb)} something {biz_adj}.",
            f"Your {biz_adj} new {noun}.We {verb}.",
            f"The evolution of the {noun}.",
            f"For those who {verb}.",
            f"Your {noun}. {capitalize_first(biz_adj)}.",
            f"Do you {verb}?",
            f"The {noun} you've been waiting for.",
            f"{capitalize_first(insp_verb)}. {capitalize_first(verb)}.",
            f"{capitalize_first(insp_verb)} your {noun}.",
            f"{capitalize_first(insps_gerund)} your {noun}.",
        ]
        return self.generator.random_element(slogan_options)

    def opener(self, industry, company_name):
        noun = self.generator.random_element(
            (self.industry_dict[industry]["NOUNS"].split(", "))
        )
        plural = self.generator.random_element(
            (self.industry_dict[industry]["PLURALS"].split(", "))
        )
        gerund = self.generator.random_element(
            (self.industry_dict[industry]["GERUNDS"].split(", "))
        )
        verb = self.generator.random_element(
            self.industry_dict[industry]["VERBS"].split(", ")
        )
        # adjective = self.generator.random_element(
        #     self.industry_dict[industry]["ADJECTIVES"].split(", ")
        # )
        biz_adj = self.generator.random_element(BIZ_ADJS)
        # biz_advb = self.generator.random_element(BIZ_ADVBS)
        insp_verb = self.generator.random_element(INSP_VERBS)
        # insps_gerund = self.generator.random_element(INSP_GRUNDS)
        opener_options = [
            f"{company_name} is revolutionizing the way people think about {noun}.",
            f"{company_name} is why you'll never {verb} the same way again.",
            f"{company_name} was created to help you find {noun} in your area. From local {noun} to national brands, no one knows {noun} like {company_name}. No one.",
            f"{company_name} is a place for people who enjoy {gerund} to connect. Find local {gerund} events or just share your favorite tips and stories with others who love to {verb}.",
            f"Share your favorite {noun} and discover new ones. With {company_name} you never know what you might find!",
            f"{company_name} was founded by people who love {gerund} just like you! Enter your favorite ways to {verb} and we'll help you fit it all in. Since we're using {biz_adj} technologies, you can count on us next time you {verb}.",
            f"{company_name} is the last word in {biz_adj} {noun}. We know you never settle for less than the best and neither do we. {verb} with professional grade tools and {insp_verb} your future.",
            f"{capitalize_first(gerund)}. Everyone talks about it but only the truly {biz_adj} are able to {verb} day in and day out. Here at {company_name} we understand your commitment and want to give you what you need to take your {gerund} to the next level.",
            f"{capitalize_first(insp_verb)} your niche in the {noun} ecosystem with online branding that's built by {biz_adj} people for {biz_adj} consumers.",
            f"{capitalize_first(insp_verb)} your niche in the {gerund} ecosystem with online branding that's built by {biz_adj} people for {biz_adj} consumers.",
            f"{company_name} is a {biz_adj} {noun} service that makes it easy to turn your {plural} into cash.",
            f"{capitalize_first(insp_verb)} & {capitalize_first(verb)} together with your team.",
            f"We use {plural} to {insp_verb} things that matter.",
            f"We're {gerund} to {insp_verb} things that matter.",
            f"Buying {plural} just got a whole lot better…",
            f"{capitalize_first(gerund)} just got a whole lot better…",
            f"Manage your organization's {plural} online, with our cloud software.",
            f"Manage your organisation's {gerund} online, with our cloud software.",
            f"Introducing the world's first {biz_adj} {noun}.",
            f"You like to {verb}. {company_name} does too.",
        ]
        return self.generator.random_element(opener_options)

    def industry(self):
        ind_weights = [float(ind["WEIGHT"]) for ind in self.industry_dict.values()]
        inds = list(self.industry_dict.keys())
        return self.weighted_choice(inds, ind_weights)

    def products(self, industry):
        return self.industry_dict[industry]["PRODUCTS"]

    def website_font_color(self):
        return self.generator.color(luminosity="light")

    def company_phone_number(self):
        return Phone(self.generator.numerify(text="(%#%) %##-####"))

    def founded(self):
        # TODO
        return 2001
        # year_range = self.generator.weighted_choice(
        #     self.founded_ranges, self.founded_weights
        # ).split("-")
        # start_year, end_year = map(int, year_range)

        # age = self.generator.random_int(start_year, end_year)
        # return self.generator.today().year - age

    def employee_structure(self, industry, scope, store):
        employee_list = []
        structs = self.industry_dict[industry]["SCOPES"][scope][store][
            "EMPLOYEE_STRUCTURE"
        ]
        for struct in structs:
            num_range = struct[0]
            role_name = struct[1]
            team_name = struct[2]
            salary = struct[3]
            num = self.generator.random_int(num_range[0], num_range[1])
            employee_list.extend(
                EmployeeRole(role_name, team_name, salary) for _ in range(num)
            )
        return employee_list

    def client_scope(self, industry):
        scopes = list(self.industry_dict[industry]["SCOPES"].keys())
        return self.random_element(scopes)

    def locations_info(self, industry, scope):
        return self.industry_dict[industry]["SCOPES"][scope]

    def client_frequency(self, industry):
        c_range = self.industry_dict[industry].get("FREQUENCY_RANGE", [0, 0])
        val = self.generator.pyint(
            min_value=c_range[0] * 100, max_value=c_range[1] * 100
        )
        return float(val / 100)

    # def market_share(self, industry, sub_industry):
    #     return round(self.generator.random.random(), 2)
