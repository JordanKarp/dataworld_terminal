import re


def natural_sort_key(s):
    """
    Generate a sorting key for natural sorting.
    Splits the string into numeric and non-numeric parts.
    """
    # Regular expression to split text into numbers and non-numbers
    return [
        int(text) if text.isdigit() else text.lower() for text in re.split(r"(\d+)", s)
    ]


def natsort(iterable):
    """
    Sorts an iterable of strings in natural order.
    """
    return sorted(iterable, key=natural_sort_key)
