
from . import game

def get_possible_move(game_data):
    if game_data["state"] == game.STATE_END: return []
    if game_data["state"] == game.STATE_CHOOSING:
        ret = []
        # for each players, each card in the hand can go to the pre_board of the player 
        for i in range(0, len(game_data["players"])):
            player = game_data["players"][i]
            if not len(player["pre_board"]):
                for card in player["hand"]:
                    ret.append({
                        "player": i,
                        "card": card,
                        "source": "hand",
                        "target": "pre_board",
                    })
        return ret
    elif game_data["state"] == game.STATE_PLAYER_TURNS:
        ret = []
        player = game_data["current_player"]
        # first we test if there is sanctuarires to choose
        # if yes, it shortcut to selection in the central board
        if len(game_data["pre_sanctuaries"]):
            # for each sanctuary in the select area (pre_sanctuary)
            # the current player can play it
            for card in game_data["pre_sanctuaries"]:
                ret.append({
                    "player": player,
                    "card": card,
                    "source": "pre_sanctuaries",
                    "target": "sanctuaries",
                })
        else: # if not we rare in the select a card from the central board sub-phase
            # for each card in the central_board
            for card in game_data["central_board"]:
                ret.append({
                    "player": player,
                    "card": card,
                    "source": "central_board",
                    "target": "hand",
                })
        return ret
    raise ValueError(f"state not implemented: {game_data['state']}")

def make_move(game_data, move, card_data, sanctuaries_data):
    print(f"***MAKE_MOVE state:{game.convert_num_to_state(game_data["state"])}    move:{move}")
    if game.STATE_CHOOSING == game_data["state"]:
        player_id = move["player"]
        #assert player == game_data["current_player"]
        card = move["card"]
        assert card in game_data["players"][player_id]["hand"]
        print("bon move")

        # check that the pre_board is not already filled
        if len(game_data["players"][move['player']]['pre_board']): raise ValueError(f"player already choose a card")

        # {'player': 0, 'card': 54, 'target': 'pre_board'}
        # retire de sa main
        print(f"before {game_data["players"][move['player']]}")
        game_data["players"][player_id]["hand"].remove(move['card'])
        game_data["players"][move['player']]['pre_board'].append(move['card'])
        print(f"after {game_data["players"][move['player']]}")

        # check if all players finished their turn
        # if yes, move to next phase and check the current player
        if all_player_have_preboard(gamedata=game_data):
            game_data["state"] = game.STATE_PLAYER_TURNS
            switch_player_for_player_turns_phase(game_data, card_data, sanctuaries_data)

        return game_data
    elif game_data["state"] == game.STATE_PLAYER_TURNS:
        player_id = move["player"]
        # check that it's the good player turn
        if player_id != game_data["current_player"]: raise ValueError(f"wrong player try to choose a card")
        
        # manage case for chossing a card from central board
        if move['source'] == "central_board":
            if len(game_data["pre_sanctuaries"]): raise ValueError("player try to continue his turn but need to select a sanctuary first")

            # take card in hand
            print(f"before {game_data["players"][move['player']]}")
            game_data["central_board"].remove(move['card'])
            game_data["players"][move['player']]['hand'].append(move['card'])
            print(f"after {game_data["players"][move['player']]}")

            # fill the board
            pre_board = game_data["players"][player_id]["pre_board"][0]
            print(f"pre_board: {pre_board} for player {player_id}")
            game_data["players"][player_id]["pre_board"].remove(pre_board)
            game_data["players"][player_id]["board"].append(pre_board)

            ret = switch_player_for_player_turns_phase(game_data, card_data, sanctuaries_data)
            # if their is no player still to play
            if ret == -1:
                # check if it's the end of the game
                # 1. board of all players are at 8
                # 2. no player need to play (territory and sanctuary are good)
                if len(game_data["players"][0]["board"]) == 8 and not len(game_data["pre_sanctuaries"]):
                    game_data["state"] = game.STATE_END
                    return

                game_data["state"] = game.STATE_CHOOSING
                game_data["off_territories"].append(game_data["central_board"][0])
                game_data["central_board"].pop()
                # fillup the board
                for i in range(0, game_data["nb_players"] + 1):
                    game_data = game.fill_central_board_one_time(game_data)
            return
        elif move['source'] == "pre_sanctuaries" and move["target"] == "sanctuaries": # player want to add a sanctuaries to their global board
            # check that the move is legal
            if move["card"] not in game_data["pre_sanctuaries"]: raise ValueError("player try to cheat sanctuary selection")
            # first add the card to the player sanctuaries
            game_data["players"][player_id]["sanctuaries"].append(move["card"])
            # then remove sanctuaries to the "off" stack
            while len(game_data["pre_sanctuaries"]):
                id = game_data["pre_sanctuaries"].pop()
                game_data["off_sanctuaries"].append(id)
            return
    raise ValueError("Not implemented")

def switch_player_for_player_turns_phase(gamedata, card_data, sanctuaries_data):
    gamedata["current_player"] = -1
    # check the player number to play first
    min_card_id = 999
    for i in range(0,len(gamedata["players"])):
        if len(gamedata["players"][i]["pre_board"]): # if the player didn't played
            min_card_id = min(min_card_id, gamedata["players"][i]["pre_board"][0])
            print(f"check player selection for first {gamedata["players"][i]["pre_board"][0]}")
            if min_card_id==gamedata["players"][i]["pre_board"][0]:
                gamedata["current_player"] = i
    player = gamedata['current_player']
    print(f"the player with the lower card is {player}")                      
    # FIXME add sanctuary selection fill up
    # 
    # 1. get stats from player
    # 2. fill the pre_sanctuaries
    if gamedata["current_player"] != -1 and (
    (len(gamedata["players"][player]["board"]) + len(gamedata["players"][player]["pre_board"]))>1) and (
    gamedata["players"][player]["pre_board"][0] > gamedata["players"][player]["board"][-1]):
        print("switch to player detected, filling the santuaries")
        player = gamedata["current_player"]
        moving_stats = {}
        for sanct_id in gamedata["players"][player]["sanctuaries"]:
            moving_stats = get_stats_from_card(sanctuaries_data, sanct_id, moving_stats)
        for card_id in gamedata["players"][player]["board"]:
            moving_stats = get_stats_from_card(card_data, card_id, moving_stats)
        moving_stats = get_stats_from_card(card_data, gamedata["players"][player]["pre_board"][0], moving_stats)
        nb_sanctuaries = moving_stats.get("number_of_map",0)+1
        print(f"number of map + 1 = {nb_sanctuaries}")
        for i in range(0,nb_sanctuaries):
            game.fill_pre_sanctuaries_one_time(gamedata)
    return gamedata["current_player"]

def all_player_have_preboard(gamedata):
    """Return true if all players selected the card to play (pre_board)"""
    if game.STATE_CHOOSING != gamedata["state"]: return False
    for player in gamedata["players"]:
        if len(player["pre_board"]) != 1: return False
    return True

def get_stats_from_card(card_data, card_id, moving_stats):
    card_type = card_data[card_id-1]
    # compute colors
    if "color" in card_type:
        key_color = f"number_of_{card_type['color']}"
        moving_stats[key_color] = moving_stats.get(key_color, 0) + 1
    # compute maps
    if card_type.get("is_map", False): moving_stats["number_of_map"] = moving_stats.get("number_of_map", 0) + 1
    # compute nights
    if "night" == card_type.get("phase", "day"): moving_stats["number_of_night"] = moving_stats.get("number_of_night", 0) + 1
    # compute resources
    if "resources" in card_type:
        for res in card_type["resources"]:
            moving_stats[f"number_of_{res}"] = moving_stats.get(f"number_of_{res}", 0) + 1
    # compute multi
    moving_stats[f"number_of_multi"] = min(
        moving_stats.get("number_of_red", 0),
        moving_stats.get("number_of_yellow", 0),
        moving_stats.get("number_of_blue", 0),
        moving_stats.get("number_of_green", 0),
    )
    return moving_stats

def requirement_logic(requirements, moving_stats, resource):
    nb_required = requirements.count(resource)
    print(f"check {resource} with requirements {nb_required}")
    return moving_stats.get(f"number_of_{resource}", 0) >= nb_required

def validate_trigger_card(card_data, card_id, moving_stats):
    card_type = card_data[card_id-1]
    if len(card_type.get("requirements", [])) == 0: return True
    # check res rock
    if not requirement_logic(card_type['requirements'], moving_stats, 'rock'): return False
    if not requirement_logic(card_type['requirements'], moving_stats, 'animal'): return False
    if not requirement_logic(card_type['requirements'], moving_stats, 'fruit'): return False
    return True

def evaluate_points_card(card_data, card_id, moving_stats):
    card_type = card_data[card_id-1]
    if not card_type.get("power"): return 0
    if "conditions" not in card_type["power"]: return card_type["power"]["points"]
    points = 0
    points_to_use = card_type["power"]["points"]
    for cond in card_type["power"]["conditions"]:
        print(f"evaluate conditions {cond} with {moving_stats.get(f"number_of_{cond}", 0)}")
        points = points + points_to_use * moving_stats.get(f"number_of_{cond}", 0)
    return points

def evaluate_points_board(card_data, board, sanctuaries_data=[], sanctuaries=[]):
    print(f"board to evaluate {board}")
    points = 0
    moving_stats = {}
    # collect stats from santuaries first 
    for j in range(len(sanctuaries)):
        print("="*20)
        print(f"s:{j}")
        sanct_id = sanctuaries[j-1]
        print(f"sanct id {sanct_id} of : {sanctuaries}")
        moving_stats = get_stats_from_card(sanctuaries_data, sanct_id, moving_stats)
        print(f"stats after taking this card into account: {moving_stats}")
    # evaluate each card
    for i in range(len(board)):
        print("="*20)
        print(f"i:{i}")
        card_id = board[-i-1]
        print(f"card id {card_id} of : {board}")
        moving_stats = get_stats_from_card(card_data, card_id, moving_stats)
        print(f"stats after taking this card into account: {moving_stats}")
        points_of_card = 0
        if validate_trigger_card(card_data, card_id, moving_stats):
            print(f"card trigger {card_id} for requirements: {card_data[card_id-1].get('requirements')}")
            points_of_card = evaluate_points_card(card_data, card_id, moving_stats)
        else:
            print(f"card do not trigger for requirements: {card_data[card_id-1].get('requirements')}")
        print(f"point de la carte: {points_of_card}")
        points = points + points_of_card
    # collect from santuaries at the end 
    for k in range(len(sanctuaries)):
        print("="*20)
        print(f"s:{k}")
        sanct_id = sanctuaries[k-1]
        print(f"sanct id {sanct_id} of : {sanctuaries}")
        points_of_card = 0
        if validate_trigger_card(sanctuaries_data, sanct_id, moving_stats):
            print(f"sancturary trigger {sanct_id} for requirements: {sanctuaries_data[sanct_id-1].get('requirements')}")
            points_of_card = evaluate_points_card(sanctuaries_data, sanct_id, moving_stats)
        else:
            print(f"card do not trigger for requirements: {sanctuaries_data[sanct_id-1].get('requirements')}")
        print(f"point de la carte: {points_of_card}")
        points = points + points_of_card
    return points
