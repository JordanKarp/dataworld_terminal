from dataclasses import dataclass
from enum import Enum, auto


class MissionStatus(str, Enum):
    OFFERED = auto()
    ACCEPTED = auto()
    IN_PROGRESS = auto()
    CORRECT = auto()
    INCORRECT = auto()
    CANCELLED = auto()
    LOCKED = auto()
    VISIBLE = auto()
    INVISIBLE = auto()


@dataclass
class Mission:
    id: str
    status: MissionStatus
    title: str
    text: str
    reward: str
    _solution: str
    # _resources: object

    def __getitem__(self, item):
        return getattr(self, item, "")
