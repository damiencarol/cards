from cards.game import create_new_game, init_game, STATE_CHOOSING


def test_new_game():
    ret = create_new_game()
    assert len(ret["sanctuaries"]) == 45


def test_new_game_and_init():
    ret = create_new_game(4)
    ret = init_game(ret)
    assert len(ret["players"]) == 4
    assert len(ret["central_board"]) == 5
    for i in range(0, len(ret["players"])):
        bd = ret["players"][i]["hand"]
        assert len(bd) == 3
        for cd in bd:
            assert cd > 0 and cd < 69
    # check it's first player turn
    assert ret["current_player"] == -1
    assert ret["state"] == STATE_CHOOSING


def test_new_game_and_init_check_board(nb_players=5):
    ret = create_new_game(nb_players=nb_players)
    ret = init_game(ret)
    assert len(ret["players"]) == nb_players
    assert len(ret["central_board"]) == nb_players + 1
