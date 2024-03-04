import uuid
from enum import Enum, auto


class DataSourceTemplate:
    def __init__(self, ds_type, ds_file):
        self.ds_type = ds_type
        self.ds_file = ds_file


class DataSourceType(Enum):
    PeopleSource = auto()
    CompanySource = auto()
    GeneralSource = auto()


class DataSource:
    def __init__(self, name, requirements, fields_list, use_id=False):
        self.name = name
        self.requirements = requirements
        self.fields_list = fields_list
        self.use_id = use_id
        self.data = []

    def check_entry_requirements(self, entry):
        if self.requirements:
            for req in self.requirements.split(","):
                print(req, hasattr(entry, req))
                if not entry[req]:
                    return False
        return True

    def add_entry(self, entry):
        if not self.check_entry_requirements(entry):
            return
        new_line = []
        if self.use_id:
            new_line.append(str(uuid.uuid4()))
        for field in self.fields_list:
            if "~" in field:
                cls, fld = field.split("~")
                if entry[cls]:
                    new_line.append(str(entry[cls][fld]))
                else:
                    new_line.append(" ")
            elif entry[field]:
                new_line.append(str(entry[field]))
            else:
                new_line.append(" ")
        self.data.append(new_line)
