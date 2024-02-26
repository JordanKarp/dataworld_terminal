from faker import Faker
from faker.providers import BaseProvider
from collections import OrderedDict

# from math import pi


class ChoicesProvider(BaseProvider):
    def weighted_choice(self, options, weights):
        return self.generator.random_elements(
            OrderedDict(zip(options, weights)), length=1, use_weighting=True
        )[0]

    def norm_dist_rand(self, mean, stdev):
        return self.generator.random.normalvariate(mean, stdev)

    def percent_check(self, percent):
        return self.generator.random.random() <= percent

    def blank_or(self, element, element_percent=0.5):
        return element if self.percent_check(element_percent) else ""
