from faker import Faker
from faker.providers import BaseProvider
from collections import OrderedDict

# from math import pi


class ChoicesProvider(BaseProvider):
    gen = Faker()

    def weighted_choice(self, options, weights):
        return self.gen.random_element(OrderedDict(zip(options, weights)))

    def norm_dist_rand(self, mean, stdev):
        return self.gen.random.normalvariate(mean, stdev)
