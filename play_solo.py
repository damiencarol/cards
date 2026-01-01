import json
from cards.game import create_new_game, init_game, STATE_CHOOSING, STATE_PLAYER_TURNS, STATE_END, convert_num_to_state
from cards.logic import get_possible_move, make_move, all_player_have_preboard, evaluate_points_board

from cards import generate_card_data, generate_sanctuaries_data

nb_players=3
game_data = create_new_game(nb_players)
game_data = init_game(game_data)

data = json.load(open("data.json"))
card_data = generate_card_data(data)
sanctuaries_data = generate_sanctuaries_data(data)

should_exit = False
while not should_exit:
    
    print(f"{game_data}")
    mvs = get_possible_move(game_data)
    # if all moves are only bots, let AI play
    ai_only = True
    for mv in mvs:
        if mv["player"] == 0:
            ai_only = False
        print(mv)

    print(f"*** STATE={convert_num_to_state(game_data['state'])}")

    if game_data["state"] == STATE_END:
        break

    if not ai_only:
        print("="*20)
        print(f"current player: {game_data["current_player"]}")
        print(f"number of players: {len(game_data["players"])}")
        print(f"central board : {game_data["central_board"]}")
        print(f"your hand     : {game_data["players"][0]["hand"]}")
        print(f"your board     : {game_data["players"][0]["board"]}")
        print(f"your pre-board : {game_data["players"][0]["pre_board"]}")
        print(f"your score so far: {evaluate_points_board(card_data, game_data["players"][0]["board"])}")

        print(f"all player selected their card to play? {all_player_have_preboard(game_data)}")


        if game_data["state"] == STATE_CHOOSING:
            print("you need to choose a card to play")
            inp = input()

            if "a" == inp: make_move(game_data, mvs[0], card_data, sanctuaries_data)
            elif "q" == inp: should_exit = True
            elif inp.isnumeric():
                card_wanted = int(inp)
                if card_wanted not in game_data["players"][0]["hand"]: print("you don't have this card!")
                else:
                    make_move(game_data, {
                        "player": 0, # in solo the player is 0
                        'card': card_wanted,
                        'source': 'hand',
                        'target': 'pre_board',
                    })
            else: raise ValueError("not implemented")
        else:
            print("you need to choose a card for your hand from central board")
            if len(game_data["pre_sanctuaries"]):
                print("you can also select a sanctuary by typing 's1' for example")
            inp = input()

            if "a" == inp: make_move(game_data, mvs[0], card_data, sanctuaries_data)
            if "q" == inp: should_exit = True
            elif inp.isnumeric():
                card_wanted = int(inp)
                if card_wanted not in game_data["central_board"]: print("you can't have this card!")
                else:
                    make_move(game_data, {
                        "player": 0, # in solo the player is 0
                        'card': card_wanted,
                        'source': 'central_board',
                        'target': 'hand',
                    })


    else:
        print(f"***AI move {mvs[0]}")
        make_move(game_data, mvs[0], card_data, sanctuaries_data)

scores = []
for i in range(0, nb_players):
    scores.append(evaluate_points_board(card_data, game_data["players"][i]["board"]))


print(f"your score so far: {scores[0]}")
for i in range(1, nb_players):
    print(f"score of player {i+1}: {scores[i]}")
