from dataclasses import dataclass


class MissionPrompt:
    template = str
    req = list
    data = dict


@dataclass
class Mission:
    id: str
    title: str
    prompt: MissionPrompt
    _solution: str
