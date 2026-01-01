from cards import load_data


def test_load():
    db = load_data("data.json")
    # assert len(db["territories"]) == 68
    assert len(db["sanctuaries"]) == 45

    for sanctuary in db["sanctuaries"]:
        if sanctuary["id"] == 32:
            assert sanctuary["color"] == "green"

        if sanctuary["id"] == 32:
            assert sanctuary["color"] == "green"

def test_load_territories():
    db = load_data("data.json")
    assert len(db["territories"]) == 68
    
    for obj in db["territories"]:
        if obj["id"] == 48:
            assert obj["color"] == "red"


def test_load_territories_integrity():
    db = load_data("data.json")
    cpt = [0 for i in range(1,69)]
    cards_tab = [0 for i in range(1,69)]
    for obj in db["territories"]:
        assert "id" in obj
        cpt[obj["id"]-1] = cpt[obj["id"]-1] + 1
        cards_tab[obj["id"]-1] = obj

    for j in range(1,69):
        assert cpt[j-1] == 1, f"cpt[{j}]=={cpt[j-1]}"
        assert "color" in cards_tab[j-1], f" {j-1} {cards_tab[j-1] } "
