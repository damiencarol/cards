import random

STATE_CHOOSING = 0 # state when players choose secretly the card
STATE_PLAYER_TURNS = 1 # player resolution (one by one)
STATE_END = 2 # end of game

def convert_num_to_state(val):
    if val == STATE_CHOOSING: return "STATE_CHOOSING"
    if val == STATE_PLAYER_TURNS: return "STATE_PLAYER_TURNS"
    if val == STATE_END: return "STATE_END"
    raise ValueError(val)

def create_new_game(nb_players=4):
    ret = {
        "state": STATE_CHOOSING,
        "pre_sanctuaries": [], # place to select card to play
        "sanctuaries": list(range(1, 46)),  # 45 sanctuaries
        "territories": list(range(1, 69)),  # 68 cards
        "off_territories": [],
        "central_board": [],
        "nb_players": nb_players,
        "players": [],
        "current_player": -1,
    }
    # init players (without data)
    for i in range(0, nb_players):
        ret["players"].append({"pre_board": [], "board": [], "hand": [], "sanctuaries": []})
    return ret


def fill_central_board_one_time(game_data):
    i = random.randint(0, len(game_data["territories"]) - 1)
    card = game_data["territories"][i]
    game_data["territories"].remove(card)
    game_data["central_board"].append(card)
    return game_data


def init_game(game_data):
    # print(game_data)
    # give 3 cards by player
    for i in range(0, game_data["nb_players"]):
        give_a_card_player(game_data, i)
        give_a_card_player(game_data, i)
        give_a_card_player(game_data, i)
        # print(f"hand of player {i}: {game_data["players"][i]}")
    # init the central board (x times + 1)
    for i in range(0, game_data["nb_players"] + 1):
        game_data = fill_central_board_one_time(game_data)
    return game_data


def give_a_card_player(game_data, player_number):
    i = random.randint(0, len(game_data["territories"]) - 1)
    card = game_data["territories"][i]
    game_data["territories"].remove(card)
    game_data["players"][player_number]["hand"].append(card)
    return game_data
