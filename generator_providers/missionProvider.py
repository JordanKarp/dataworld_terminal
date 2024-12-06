from pathlib import Path

from classes.mission import Mission

from generator_providers.choicesProvider import ChoicesProvider
from utilities.load_tools import load_weighted_csv, load_json

MISSION_DATA_PATH = Path("./data/animal/master_pets.json")


class MissionProvider(ChoicesProvider):
    mission_data = load_json(MISSION_DATA_PATH)

    def mission(self, mission_type):

        data = self.random_element(self.mission_data[mission_type])

        return Mission(id, title, text, solution)
