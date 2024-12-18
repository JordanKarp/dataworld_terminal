from faker.providers import BaseProvider
from collections import OrderedDict
import numpy as np


class ChoicesProvider(BaseProvider):
    def weighted_choice(self, options, weights):
        return self.generator.random_elements(
            OrderedDict(zip(options, weights)), length=1, use_weighting=True
        )[0]

    def norm_dist_rand(self, mean, stdev):
        return self.generator.random.normalvariate(mean, stdev)

    # TODO test this
    def lognorm_dist_rand(self, mean, sigma):
        mu = np.log(mean**2 / np.sqrt(sigma**2 + mean**2))
        s = np.sqrt(np.log(1 + (sigma**2 / mean**2)))

        # Generate a random number from the log-normal distribution
        return self.generator.random.lognormal(mu, s)

    def percent_check(self, percent):
        return self.generator.random.random() <= percent

    def blank_or(self, element, element_percent=0.5):
        return element if self.percent_check(element_percent) else ""
