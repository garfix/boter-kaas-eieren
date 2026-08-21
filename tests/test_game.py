from boter_kaas_eieren.game import Game


def test_players_take_turns_and_can_win() -> None:
    game = Game()
    for position in (0, 3, 1, 4, 2):
        game.move(position)

    assert game.winner == "X"
    assert game.current_player == "O"


def test_full_board_without_winner_is_draw() -> None:
    game = Game()
    for position in (0, 1, 2, 4, 3, 5, 7, 6, 8):
        game.move(position)

    assert game.winner is None
    assert game.is_draw


def test_cannot_play_taken_square() -> None:
    game = Game()
    game.move(0)

    try:
        game.move(0)
    except ValueError as error:
        assert str(error) == "that square is already taken"
    else:
        raise AssertionError("expected a taken-square error")
