import json

def load_json(json_name):
    data = {}

    with open(json_name) as file:
        data = json.load(file)

    return data