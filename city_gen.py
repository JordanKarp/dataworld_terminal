from address_gen import *

NUM_ROADS = 5
SIZE = 100
COMM_TO_RES = 0.25


def gen_city(size, num_roads):
    roads = []
    for i in range(1, num_roads + 1):
        road = ""
        while road not in roads or road != "":
            road = gen_street_names()
