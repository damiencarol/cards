import json
from cards import game
from cards import logic

from cards import load_data, generate_card_data, generate_sanctuaries_data

def test_possible_moves():
    ret = game.create_new_game(4)
    ret = game.init_game(ret)
    mvs = logic.get_possible_move(ret)
    assert len(mvs) == 12
    ret = game.create_new_game(3)
    ret = game.init_game(ret)
    mvs = logic.get_possible_move(ret)
    assert len(mvs) == 9
    ret = game.create_new_game(5)
    ret = game.init_game(ret)
    mvs = logic.get_possible_move(ret)
    assert len(mvs) == 15


ret1 = {
    "state": 0, # player choosing
    "sanctuaries": [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        30,
        31,
        32,
        33,
        34,
        35,
        36,
        37,
        38,
        39,
        40,
        41,
        42,
        43,
        44,
        45,
    ],
    "territories": [
        1,
        3,
        4,
        5,
        6,
        7,
        9,
        11,
        12,
        14,
        15,
        16,
        17,
        18,
        19,
        21,
        22,
        23,
        24,
        26,
        27,
        29,
        30,
        31,
        33,
        34,
        36,
        37,
        40,
        41,
        42,
        43,
        44,
        45,
        49,
        51,
        52,
        54,
        56,
        57,
        58,
        59,
        60,
        61,
        62,
        63,
        64,
        65,
        66,
        67,
        68,
    ],
    "central_board": [10, 28, 50, 25, 38],
    "nb_players": 4,
    "players": [
        {"board": [], "hand": [39, 32, 48], "pre_board": []},
        {"board": [], "hand": [8, 13, 53], "pre_board": []},
        {"board": [], "hand": [47, 55, 35], "pre_board": []},
        {"board": [], "hand": [2, 20, 46], "pre_board": []},
    ],
    "current_player": -1,
}


def test_possible_moves_with_fixed_data():
    ret = ret1
    mvs = logic.get_possible_move(ret)
    for i in range(0, 3):
        print(mvs[i])
        assert mvs[i]["card"] in ret["players"][mvs[i]["player"]]["hand"]

def test_make_a_move_with_fixed_data():
    ret = ret1
    mvs = logic.get_possible_move(ret)
    # checks
    assert len(mvs) == 12
    for i in range(0, len(mvs)-1):
        player = mvs[i]["player"]
        assert mvs[i]["card"] in ret["players"][player]["hand"]

def test_evaluate_20_31_27():
    db = load_data("data.json")
    card_data = generate_card_data(db)
    board = [20, 31, 27]
    assert 3 == logic.evaluate_points_board(card_data, board, [])

def test_evaluate_37_39():
    db = load_data("data.json")
    card_data = generate_card_data(db)
    board = [37,39]
    assert 6 == logic.evaluate_points_board(card_data, board, [])


def test_evaluate_54_4_14():
    evaluate_params([54, 4, 14], [], 0)

def test_evaluate_9_5():
    evaluate_params([9, 5], [], 7)
def test_evaluate_5():
    evaluate_params([5], [], 2)
def test_evaluate_9():
    evaluate_params([9], [], 5)
def test_evaluate_30():
    evaluate_params([30], [], 2)
def test_evaluate_30_31():
    evaluate_params([30, 31], [], 3)


def test_evaluate_8cards():
    evaluate_params([1,2,3,4,5,6,7,8], [], 6)

def test_evaluate_8cards_random():
    board=[62, 54, 11, 40, 55, 56, 42, 25]
    evaluate_params(board, [], 3)

def test_evaluate_8cards_random_with_sanctuary():
    board=[62, 54, 11, 40, 55, 56, 42, 25]
    sancts=[3] # 3 have one animal
    evaluate_params(board, sancts, 11)

"""
def test_evaluate_8cards_random_with_sanctuaries():
    board=[62, 54, 11, 40, 55, 56, 42, 25]
    sancts=[3, 42] # 3 have one animal, 42 have fruit and red
    evaluate_params(board, sancts, 11)
"""

def test_evaluate_cards_random_with_multi_color():
    board=[43, 59, 18, 19]
    sancts=[]
    evaluate_params(board, sancts, 12)

def test_evaluate_cards_random2():
    board=[33, 27, 11, 14, 40, 20, 43, 4]
    sancts=[]
    evaluate_params(board, sancts, 17)

def test_evaluate_cards_random2_with_sanct():
    board=[33, 27, 11, 14, 40, 20, 43, 4]
    sancts=[11]
    evaluate_params(board, sancts, 23)
    

def evaluate_params(board, sanctuaries, points):
    db = load_data("data.json")
    card_data = generate_card_data(db)
    sanctuaries_data = generate_sanctuaries_data(db)
    assert points == logic.evaluate_points_board(card_data, board, sanctuaries_data, sanctuaries)

def test_complete_game():
    db = load_data("data.json")
    card_data = generate_card_data(db)
    sanctuaries_data = generate_sanctuaries_data(db)
    
    ret = game.create_new_game(4)
    ret = game.init_game(ret)

    while ret["state"] != game.STATE_END:
        mvs = logic.get_possible_move(ret)
        logic.make_move(ret, mvs[0], card_data, sanctuaries_data)
