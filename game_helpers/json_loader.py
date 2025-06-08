import json

def load_json_file(json_path):
    with open(json_path, 'r') as f:
        return json.load(f)