from boter_kaas_eieren.game import Game
from boter_kaas_eieren.models.MonteCarloTreeSearch import MonteCarloTreeSearch


def test_returns_none_when_game_is_over() -> None:
    game = Game()
    game.move(0)
    game.move(3)
    game.move(1)
    game.move(4)
    game.move(2)

    policy = MonteCarloTreeSearch(game, iterations=10)
    assert policy.best_move() is None


def test_returns_a_legal_move_on_an_empty_board() -> None:
    policy = MonteCarloTreeSearch(Game(), iterations=100, seed=1)
    move = policy.best_move()
    assert move is not None
    assert 0 <= move < 9


def test_returns_a_legal_move_mid_game() -> None:
    game = Game()
    game.move(0)
    game.move(1)

    policy = MonteCarloTreeSearch(game, iterations=200, seed=2)
    move = policy.best_move()
    assert move in (2, 3, 4, 5, 6, 7, 8)


def test_takes_an_available_win() -> None:
    # X can complete a diagonal by playing square 8 and must take it.
    game = Game()
    game.move(0)
    game.move(2)
    game.move(4)
    game.move(3)
    # current_player is X again, board: X O . / . X . / O . .
    assert game.winner() is None

    policy = MonteCarloTreeSearch(game, iterations=500, seed=3)
    assert policy.best_move() == 8