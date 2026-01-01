import json

def load_data(file):
    with open(file) as fp:
        return json.load(fp)

def generate_card_data(db):
    ls = list(range(1,69))
    for card in db["territories"]:
        ls[card["id"] - 1] = card
    return ls

def generate_sanctuaries_data(db):
    ls = list(range(1,46))
    for card in db["sanctuaries"]:
        ls[card["id"] - 1] = card
    return ls
