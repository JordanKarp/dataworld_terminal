import csv


def load_txt(file_name):
    with open(file_name, "r") as text_file:
        lines = [line.strip() for line in text_file]
        return lines


def load_csv(file_name):
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        return list(csv_reader)


def load_weighted_csv(file_name):
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        options = []
        weights = []
        for data, weight in csv_reader:
            options.append(str(data))
            weights.append(float(weight))
        return options, weights
