def objects_to_table(obj_dict):
    # Get the first object's attributes for the header
    headers = list(obj_dict[next(iter(obj_dict))].__dict__.keys())

    # Initialize the table with the header row
    table = [headers]

    # Iterate over the dictionary and add each object's values as a row
    for obj in obj_dict.values():
        row = [getattr(obj, attr) for attr in headers]
        table.append(row)

    return table
