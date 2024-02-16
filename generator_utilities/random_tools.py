from random import normalvariate, choices, random


# def weighted_random(options, weights, num=1):
#     return choices(options, weights, k=num)


def norm_dist_rand(mean, st_dv):
    return normalvariate(mean, st_dv)


def blank_or(element, element_percent=0.5):
    if random() <= element_percent:
        return element
    return ""
