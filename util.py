import json


def print_json_to_pretty(o):
    return print(json.dumps(o, indent=2, ensure_ascii=False))