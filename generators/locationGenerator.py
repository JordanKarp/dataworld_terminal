from faker import Faker
import json

from classes.location import Location


class LocationGenerator:
    def __init__(self, seed=None):
        self.gen = Faker()
        if seed:
            Faker.seed(seed)

    def generate_locations_from_town(self, town_file):
        with open(town_file) as f:
            data = json.load(f)
            city = data.get("NAME", "UnknownCity")
            state = data.get("STATE", "UnknownState")
            roads = data.get("ROADS", {})
            map_rows = int(data.get("MAP_ROWS", 15))
            map_cols = int(data.get("MAP_COLS", 90))

        dimensions = (map_rows, map_cols)
        new_roads = []
        locations = []
        for road, elements in roads.items():
            road_row = int(elements.get("START_ROW", 0))
            road_col = int(elements.get("START_COL", 0))
            road_is_vert = elements.get("IS_VERT", "True") == "True"
            road_length = int(elements.get("LENGTH", 3))
            new_roads.append((road, road_row, road_col, road_is_vert, road_length))
            for num, building in elements.get("LOCATIONS", {}).items():
                building_type = building.get("BUILDING_TYPE", "Residence")
                value = building.get("VALUE", 0)
                lot_size = building.get("LOT_SIZE", 0)
                a1s = []
                if "R" in num:
                    start_num = int(building.get("START_NUM", 0))
                    end_num = int(building.get("END_NUM", 0))
                    inc_num = int(building.get("INC_NUM", 1))
                    a1s = self.gen_address_ones(road, start_num, end_num, inc_num)
                else:
                    a1s = [f"{num} {road}"]

                a2_type = building.get("ST_2_NUMBER_TYPE", None)

                a2s = [""]
                if a2_type:
                    start_unit = int(building.get("START_UNIT"), 0)
                    end_unit = int(building.get("END_UNIT"), 0)
                    start_floor = int(building.get("START_FLOOR"), 0)
                    end_floor = int(building.get("END_FLOOR"), 0)
                    a_2_text = building.get("ST_2_TEXT", "Apt.")
                    skip_13 = building.get("SKIP_13", "") not in [
                        "False",
                        "false",
                        "FALSE",
                        False,
                    ]
                    a2s = self.gen_address_twos(
                        a2_type,
                        start_unit,
                        end_unit,
                        start_floor,
                        end_floor,
                        a_2_text,
                        skip_13,
                    )

                for a1 in a1s:
                    locations.extend(
                        Location(
                            street_address_1=a1,
                            street_address_2=a2,
                            city=city,
                            state=state,
                            building_type=building_type,
                            value=value,
                            lot_size=lot_size,
                        )
                        for a2 in a2s
                    )

        return locations, new_roads, dimensions

    def gen_unit_nums(self, unit_start, unit_end):
        return list(range(unit_start, unit_end + 1))

    def gen_floor_nums(self, floor_first, floor_top, skip_13=True):
        return [
            str(i) for i in range(floor_first, floor_top + 1) if i != 13 or not skip_13
        ]

    def numbering_types(
        self,
        n_type,
        start_unit,
        end_unit,
        start_floor=None,
        end_floor=None,
        skip_13=True,
    ):
        if n_type == "A":
            """# - Apt 1"""
            return self.gen_unit_nums(start_unit, end_unit)
        if n_type == "B":
            """F# - Apt 11"""
            return [
                f"{floor}{unit}"
                for floor in self.gen_floor_nums(start_floor, end_floor, skip_13)
                for unit in self.gen_unit_nums(start_unit, end_unit)
            ]
        if n_type == "C":
            """F## - Apt 101"""
            return [
                f"{floor}{unit:02}" if int(floor) >= 1 else unit
                for floor in self.gen_floor_nums(start_floor, end_floor, skip_13)
                for unit in self.gen_unit_nums(start_unit, end_unit)
            ]
        if n_type == "D":
            """FC - Apt 1A"""
            return [
                f"{floor}{chr(unit + 64)}"
                for floor in self.gen_floor_nums(start_floor, end_floor, skip_13)
                for unit in self.gen_unit_nums(start_unit, end_unit)
            ]
        if n_type == "E":
            """CF - Apt A1"""
            return [
                f"{chr(unit + 64)}{floor}"
                for floor in self.gen_floor_nums(start_floor, end_floor, skip_13)
                for unit in self.gen_unit_nums(start_unit, end_unit)
            ]
        if n_type == "F":
            """C - Apt A"""
            return [chr(i + 64) for i in self.gen_unit_nums(start_unit, end_unit)]

    def gen_address_ones(self, road, start, end, inc):
        return [f"{a1} {road}" for a1 in range(start, end + 1, inc)]

    def gen_address_twos(
        self, a2_type, start_unit, end_unit, start_floor, end_floor, a_2_text, skip_13
    ):
        nums = (
            self.numbering_types(
                a2_type, start_unit, end_unit, start_floor, end_floor, skip_13
            )
            or []
        )

        if a_2_text == "" or a_2_text is None:
            return [f"{num}" for num in nums]
        else:
            return [f"{a_2_text} {num}" for num in nums]
