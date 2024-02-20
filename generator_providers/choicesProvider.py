from faker import Faker
from faker.providers import BaseProvider
from collections import OrderedDict

# from math import pi


class ChoicesProvider(BaseProvider):
    def weighted_choice(self, options, weights):
        return self.generator.random_element(OrderedDict(zip(options, weights)))

    def norm_dist_rand(self, mean, stdev):
        return self.generator.random.normalvariate(mean, stdev)
