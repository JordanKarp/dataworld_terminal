from enum import Enum
from dataclasses import dataclass


class MapIcons(str, Enum):
    ROAD_VERT = "│"
    ROAD_HORIZ = "─"
    ROAD_TR_CORNER = "┐"
    ROAD_TL_CORNER = "┌"
    ROAD_BR_CORNER = "┘"
    ROAD_BL_CORNER = "└"
    ROAD_T_DOWN = "┬"
    ROAD_T_UP = "┴"
    ROAD_T_LEFT = "┤"
    ROAD_T_RIGHT = "├"
    ROAD_CROSS = "┼"
    ROAD_2_VERT = "║"
    ROAD_2_HORIZ = "═"
    ROAD_2_TR_CORNER = "╗"
    ROAD_2_TL_CORNER = "╔"
    ROAD_2_BR_CORNER = "╝"
    ROAD_2_BL_CORNER = "╚"
    ROAD_2_T_DOWN = "╦"
    ROAD_2_T_UP = "╩"
    ROAD_2_T_LEFT = "╣"
    ROAD_2_T_RIGHT = "╠"
    ROAD_2_CROSS = "╬"
    ROAD_MIX_T_RIGHT = "╞"
    ROAD_MIX_T_LEFT = "╡"
    ROAD_MIX_T_UP = "╨"
    ROAD_MIX_T_DOWN = "╥"
    EMPTY = " "
    SFU = "■"
    MFU = "█"
    RETAIL = "□"

    def __str__(self) -> str:
        return str.__str__(self)


@dataclass
class MapCell:
    row: int = 0
    col: int = 0
    data: str = ""
    icon: MapIcons = MapIcons.EMPTY
