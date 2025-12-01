
from cards import load_data

def test_load():
    db = load_data("data.json")
    #assert len(db["territories"]) == 68
    assert len(db["sanctuaries"]) == 45

    for sanctuary in db["sanctuaries"]:
        if sanctuary["id"] == 32:
            assert sanctuary["color"] == "green"
