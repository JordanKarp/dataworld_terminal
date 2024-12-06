import json
from dataclasses import dataclass


# TOWN_FILE = "green_lake.json"
# TOWN_FILE = "baxter_center_jk.json"
TOWN_FILE = "bridgewater_city.json"


@dataclass
class Location:
    a_1: str
    a_2: str
    city: str
    state: str
    loc_type: str

    def __str__(self):
        if self.a_2 != "":
            return f"{self.loc_type}: {self.a_1}, {self.a_2}, {self.city}, {self.state}"
        else:
            return f"{self.loc_type}: {self.a_1}, {self.city}, {self.state}"


def gen_unit_nums(unit_start, unit_end):
    return list(range(unit_start, unit_end + 1))


def gen_floor_nums(floor_first, floor_top, skip_13=True):
    return [str(i) for i in range(floor_first, floor_top + 1) if i != 13 or not skip_13]


def numbering_types(
    n_type, start_unit, end_unit, start_floor=None, end_floor=None, skip_13=True
):
    if n_type == "A":
        """# - Apt 1"""
        return gen_unit_nums(start_unit, end_unit)
    if n_type == "B":
        """F# - Apt 11"""
        return [
            f"{floor}{unit}"
            for floor in gen_floor_nums(start_floor, end_floor, skip_13)
            for unit in gen_unit_nums(start_unit, end_unit)
        ]
    if n_type == "C":
        """F## - Apt 101"""
        return [
            f"{floor}{unit:02}" if int(floor) >= 1 else unit
            for floor in gen_floor_nums(start_floor, end_floor, skip_13)
            for unit in gen_unit_nums(start_unit, end_unit)
        ]
    if n_type == "D":
        """FC - Apt 1A"""
        return [
            f"{floor}{chr(unit + 64)}"
            for floor in gen_floor_nums(start_floor, end_floor, skip_13)
            for unit in gen_unit_nums(start_unit, end_unit)
        ]
    if n_type == "E":
        """CF - Apt A1"""
        return [
            f"{chr(unit + 64)}{floor}"
            for floor in gen_floor_nums(start_floor, end_floor, skip_13)
            for unit in gen_unit_nums(start_unit, end_unit)
        ]
    if n_type == "F":
        """C - Apt A"""
        return [chr(i + 64) for i in gen_unit_nums(start_unit, end_unit)]


def gen_address_ones(road, start, end, inc):
    return [f"{a1} {road}" for a1 in range(start, end + 1, inc)]


def gen_address_twos(
    a2_type, start_unit, end_unit, start_floor, end_floor, a_2_text, skip_13
):
    nums = (
        numbering_types(a2_type, start_unit, end_unit, start_floor, end_floor, skip_13)
        or []
    )

    if a_2_text == "" or a_2_text is None:
        return [f"{num}" for num in nums]
    else:
        return [f"{a_2_text} {num}" for num in nums]


def parse_locations(roads, city, state):
    locations = []
    for road, buildings in roads.items():
        for num, building in buildings.items():
            building_type = building.get("BUILDING_TYPE")
            a1s = []
            if "R" in num:
                start_num = int(building.get("START_NUM", 0))
                end_num = int(building.get("END_NUM", 0))
                inc_num = int(building.get("INC_NUM", 1))
                a1s = gen_address_ones(road, start_num, end_num, inc_num)
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
                a2s = gen_address_twos(
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
                        a_1=a1, a_2=a2, city=city, state=state, loc_type=building_type
                    )
                    for a2 in a2s
                )
    return locations


def read_town_json():  # sourcery skip: use-named-expression
    with open(TOWN_FILE) as f:
        data = json.load(f)
        city = data.get("NAME")
        state = data["STATE"]
        roads = data["ROADS"]

    return roads, city, state


def write_to_results_file(locations):
    with open("results.txt", "w") as f:
        for loc in locations:
            f.write(f"{loc}\n")


def print_results(locations):
    for loc in locations:
        print(loc)


def get_location_counts(locations):
    count_dict = {}
    for location in locations:
        # count_dict[location.loc_type] = count_dict.get("loc_type", 0) + 1
        location_type = location.loc_type
        if location_type in count_dict:
            count_dict[location_type] += 1
        else:
            count_dict[location_type] = 1
    return count_dict


def main():
    roads, town, city = read_town_json()

    locations = parse_locations(roads, town, city)
    write_to_results_file(
        locations,
    )

    # Uncomment below if you want to print results rather than create a results file.
    # print_results(locations)

    counts = get_location_counts(locations)
    print(counts)


if __name__ == "__main__":
    main()
