from dataclasses import dataclass


@dataclass
class DataSource:
    def __init__(self, name, fields, data=None):
        self.name = name
        self.fields = fields
        self.data = data or []
