from ast import literal_eval
import csv
from faker import Faker
from pathlib import Path

from classes.mission import Mission, MissionStatus
from utilities.load_tools import load_csv

STARTER_MISSIONS = 2
# MISSION_DATA_PATH = Path("mission_prototypes.tsv")
MISSION_DATA_PATH = Path("prototypes2.tsv")


class MissionGenerator:
    def __init__(self, pop, comp, seed=None):
        self.gen = Faker()
        if seed:
            Faker.seed(seed)
        self.population = pop
        self.companies = comp
        self.counter = 1
        self.missions = {}

        self.mission_data = load_csv(MISSION_DATA_PATH, delim="\t")

    def generate_missions(self, num=STARTER_MISSIONS):
        for _ in range(num):
            if mission := self.new_mission():
                self.missions[mission.id] = mission
        return self.missions

    def new_mission(self):
        mission_prototype = self.gen.random_element(self.mission_data)
        reqs = literal_eval(mission_prototype[4])
        # print(reqs)
        guilty = None
        # TODO adjust so that I can add values, ex. vehicle.color == 'Red'
        # TODO adjust so that I check more than just persons

        # pop = [
        #     p
        #     for p in self.population.values()
        #     if all(getattr(p, req, None) for req in reqs if isinstance(req, str))
        # ]

        pop = []
        for p in self.population.values():
            meets_all_reqs = True
            for req in reqs:
                if isinstance(req, str):
                    if not getattr(p, req, None):
                        meets_all_reqs = False
                        break
                if isinstance(req, list):
                    params = req[0].split(".")
                    value = p
                    for param in params:
                        value = getattr(value, param, None)
                        if value is None:
                            break
                    if value != req[1]:
                        meets_all_reqs = False
                        break

            if meets_all_reqs:
                pop.append(p)

        # pop = []
        # for p in self.population.values():
        #     valid = True
        #     for req in reqs:
        #         if isinstance(req, str) and hasattr(p, req):
        #             valid = False
        #             break
        #         # if (
        #         #     isinstance(req, list)
        #         #     and hasattr(p, req[0])
        #         #     and getattr(p, req[0], None) != req[1]
        #         # ):
        #         #     valid = False
        #         #     break
        #     if valid:
        #         pop.append(p)

        if pop:
            guilty = self.gen.random_element(pop)
        if not guilty:
            return

        # adjust mission title, text, solution, and resources
        m_title = mission_prototype[0].format(guilty=guilty)
        m_text = mission_prototype[1].format(guilty=guilty)
        m_solution = mission_prototype[3].format(guilty=guilty)
        mission = Mission(
            id=f"M{self.counter}",
            status=MissionStatus.OFFERED,
            title=m_title,
            text=m_text,
            reward=mission_prototype[2],
            _solution=m_solution,
            # _resources=guilty,
        )
        self.counter += 1

        return mission
