
import json

def get_card(data, card_number):
    for card in data["territories"]:
        if card["id"] == card_number:
            return card
    return None

def print_card(card):
    if card is None:
        print("no card !")
        return

    print("="*10)
    print(f"id: {card['id']}")
    print(f"(m) is map: {card.get('is_map')}")
    print(f"(p) phase : {card.get('phase', 'day')}")
    print(f"(c) color : {card.get('color')}")

    if card.get("resources"):
        print(f"(r0) resource(0): {card['resources'][0]}")
        if len(card.get("resources", []))>1:
            print(f"(r1) resource(1): {card['resources'][1]}")

    if card.get("power"):
        print(f"points: {card['power'].get('points')}")

    print("="*10)

DB_FILE_NAME="data.json"
data = json.load(open(DB_FILE_NAME))

print("DB maintenance program")

print(f"nb of cards {len(data['territories'])}")

current_card = 1
exit = False
while not exit:
    # print(f"current card = {current_card}")
    card = get_card(data, current_card)
    print_card(card)

    key_name = input("\n\noption? \n q = quit \n n = new \n s = save data \n c = change color \n")

    if "q" == key_name:
        exit = True
    if "n" == key_name:
        card = {"id": current_card}
        data["territories"].append(card)

    if "p" == key_name:
        if "day" == card.get("phase", "day"):
            card["phase"] = "night"
        else:
            del card["phase"]

    if "m" == key_name:
        if card.get("is_map"):
            card["is_map"] = False
        else:
            card["is_map"] = True

    if "c" == key_name:
        if "green" == card.get("color"):
            card["color"] = "yellow"
        elif "yellow" == card.get("color"):
            card["color"] = "red"
        elif "red" == card.get("color"):
            card["color"] = "blue"
        elif "blue" == card.get("color"):
            card["color"] = "green"
        else:
            card["color"] = "green"
    if "r" == key_name:
        if card.get("resources") is None:
            card["resources"] = ["rock"]
        elif len(card["resources"]) == 0:
            card["resources"] = ["rock"]
        elif "rock" == card["resources"][0]:
            card["resources"][0] = "fruit"
        elif "fruit" == card["resources"][0]:
            card["resources"][0] = "animal"
        elif "animal" == card["resources"][0]:
            card["resources"].remove("animal")
        else:
            card["resources"][0] = "rock"
    if "t" == key_name:
        if card.get("resources") is None:
            card["resources"] = ["rock", "rock"]
        elif len(card["resources"]) == 0:
            card["resources"] = ["rock", "rock"]
        elif len(card["resources"]) < 2:
            card["resources"].append("rock")
        elif "rock" == card["resources"][1]:
            card["resources"][1] = "fruit"
        elif "fruit" == card["resources"][1]:
            card["resources"][1] = "animal"
        elif "animal" == card["resources"][1]:
            card["resources"].remove("animal")
        else:
            card["resources"][1] = "rock"
    
    if "+" == key_name:
        if "power" not in card:
            card["power"] = {"points": 1}
        else:
            if "points" not in card["power"]:
                card["power"]["points"] = 1
            else:
                card["power"]["points"] = card["power"]["points"] + 1
    if "-" == key_name:
        if "power" not in card:
            card["power"] = {"points": 1}
        else:
            if "points" not in card["power"]:
                card["power"]["points"] = 1
            else:
                card["power"]["points"] = card["power"]["points"] - 1

    if "s" == key_name:
        json.dump(data, open(DB_FILE_NAME, "w"))
        print("data saved")
    if key_name.isnumeric():
        current_card = int(key_name)
