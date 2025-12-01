
import json

def load_data(file):
    with open(file) as fp:
        return json.load(fp)
