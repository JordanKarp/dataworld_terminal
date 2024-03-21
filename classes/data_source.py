import uuid
from enum import Enum, auto
from dataclasses import dataclass


@dataclass
class DataSource:
    def __init__(self, name, fields, data=None):
        self.name = name
        self.fields = fields
        self.data = data or []


# @dataclass
# class DataSource:
#     def __init__(self, name, requirements, output_type, fields, use_id=False):
#         self.name = name
#         self.requirements = requirements
#         self.output_type = output_type
#         self.fields = fields
#         self.use_id = use_id
#         self.data = []

#     def check_entry_requirements(self, entry):
#         if self.requirements:
#             for req in self.requirements.split(","):
#                 # if not entry[req]:
#                 # print("req:", entry[req], hasattr(entry, req))
#                 if not hasattr(entry, req) or getattr(entry, req) is None:
#                     return False
#         return True

#     def print_source(self):
#         print(self.data)

#     def add_entry(self, entry):
#         if not self.check_entry_requirements(entry):
#             return
#         new_line = []
#         if self.use_id:
#             new_line.append(str(uuid.uuid4()))
#         for field in self.fields:
#             if "~" in field:
#                 cls, fld = field.split("~")
#                 if entry[cls]:
#                     new_line.append(str(entry[cls][fld]))
#                 else:
#                     new_line.append(" ")
#             elif entry[field]:
#                 new_line.append(str(entry[field]))
#             else:
#                 new_line.append(" ")
#         self.data.append(new_line)
