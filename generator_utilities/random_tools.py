from random import normalvariate, choices


def weighted_random(options, weights, num=1):
    return choices(options, weights, k=num)


def norm_dist_rand(mean, st_dv):
    return normalvariate(mean, st_dv)
