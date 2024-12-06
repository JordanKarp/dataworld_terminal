from faker import Faker
from utilities.natsort import natsort

from classes.map_cell import MapIcons, MapCell


class MapGenerator:
    def __init__(self, seed=None):
        self.gen = Faker()
        if seed:
            Faker.seed(seed)

    def create(self, locations, roads, dimensions):
        new_map_data = {}
        new_map_data = self.create_empty_map(new_map_data, dimensions)
        new_map_data = self.draw_roads(new_map_data, roads)
        new_map_data = self.draw_locations(new_map_data, locations, roads)
        # self.print_map(new_map_data)
        return new_map_data

    def create_empty_map(self, map_data, dimensions):
        rows, cols = dimensions
        for row in range(rows):
            map_data[row] = {}
            for col in range(cols):
                map_data[row][col] = None
        return map_data

    def draw_roads(self, map_data, roads):
        for road in roads:
            name = road[0]
            row_start = road[1]
            col_start = road[2]
            is_vert = road[3]
            length = road[4]

            for i in range(length):
                row_add = 0
                col_add = 0

                if is_vert:
                    row_add = i
                    icon = MapIcons.ROAD_2_VERT
                else:
                    col_add = i
                    icon = MapIcons.ROAD_2_HORIZ

                row = row_start + row_add
                col = col_start + col_add

                if map_data[row][col] is not None and map_data[row][col].icon in [
                    MapIcons.ROAD_2_VERT,
                    MapIcons.ROAD_2_HORIZ,
                ]:
                    icon = MapIcons.ROAD_2_CROSS

                cell = MapCell(row, col, name, icon)

                map_data[row][col] = cell

        return map_data

    def draw_locations(self, map_data, locations, roads):
        for location in locations:
            ad_1 = location["street_address_1"]
            ad_2 = location["street_address_2"]
            city = location["city"]
            state = location["state"]
            zipcode = location["zipcode"]
            country = location["country"]
            building_type = location["building_type"]
            value = location["value"]
            lot_size = location["lot_size"]
            checkin_log = location["checkin_log"]

            row, col = self.determine_location(ad_1, roads)

            if map_data[row][col] is not None:
                map_data[row][col].data += "\n" + location.short_addr
                # print(f"did not draw {location}")
                continue
            data = location.short_addr

            if building_type == "Residence":
                icon = MapIcons.MFU
            else:
                icon = MapIcons.RETAIL

            cell = MapCell(row, col, data, icon)
            map_data[row][col] = cell

            # print("\n".join(natsort((map_data[row][col].data.split("\n")))))
        return map_data

    def determine_location(self, address_one, roads):
        road_dict = {}
        row = 0
        col = 0
        for road in roads:
            road_dict[road[0]] = road
        number, street = address_one.split(" ", 1)

        number = int(number)

        is_even = False
        if number % 2 == 0:
            is_even = True

        if street in road_dict:
            # If street is vertical
            if road_dict[street][3]:
                if is_even:
                    row = number // 2
                    col = road_dict[street][2] - 1
                else:
                    row = number // 2
                    col = road_dict[street][2] + 1
            # If street is horizontal
            else:
                if is_even:
                    col = number // 2
                    row = road_dict[street][1] - 1
                else:
                    col = number // 2
                    row = road_dict[street][1] + 1
        return row, col

    def return_map(self, map_data):
        map_string = ""
        for row, data in map_data.items():
            for col, cell in data.items():
                map_string += cell.icon if cell is not None else " "
            map_string += "\n"
        return map_string

    def print_map(self, map_data):
        print(self.return_map(map_data))
