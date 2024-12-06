import csv
import json


def load_txt(file_name):
    with open(file_name, "r") as text_file:
        return [line.strip() for line in text_file]


def load_json(file_name):
    with open(file_name) as f:
        return json.load(f)


def load_csv(file_name, delim=","):
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=delim)
        return list(csv_reader)


def load_csv_as_dict(file_name):
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        data = {}
        for row in csv_reader:
            data[row[0]] = row[1:]
        return data


def load_weighted_csv(file_name):
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        options = []
        weights = []
        for data, weight in csv_reader:
            options.append(str(data))
            weights.append(float(weight))
        return options, weights
