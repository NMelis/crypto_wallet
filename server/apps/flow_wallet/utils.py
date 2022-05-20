import re


def to_snake(s):
    return re.sub('([A-Z]\w+$)', '_\\1', s).lower()


def convert_dict(d):
    if isinstance(d, list):
        return [convert_dict(i) if isinstance(i, (dict, list)) else i for i in d]
    return {to_snake(a): convert_dict(b) if isinstance(b, (dict, list)) else b for a, b in d.items()}
