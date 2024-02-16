import uuid


class DataSource:
    def __init__(self, name, fields_list, use_id=False):
        self.name = name
        self.fields_list = fields_list
        self.use_id = use_id
        self.data = []

    def add_entry(self, entry):
        new_line = []
        if self.use_id:
            new_line.append(str(uuid.uuid4()))
        for field in self.fields_list:
            if "~" in field:
                cls, fld = field.split("~")
                if entry[cls]:
                    new_line.append(str(entry[cls][fld]))
            elif entry[field]:
                new_line.append(str(entry[field]))
            else:
                new_line.append(" ")
        self.data.append(new_line)

    def print_source(self):
        print(self.name)
        print(self.fields_list)
        print("-" * len(self.name))
        # print(self.data)
        for num, entry in enumerate(self.data, 1):
            print(f"{num}. ", end="")
            print(" | ".join(entry))
        print()
