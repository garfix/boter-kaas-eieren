"""Terminal interface for boter-kaas-en-eieren."""

from boter_kaas_eieren.models.MiniMax import MiniMax

from .game import Game


def render(game: Game) -> str:
    """Render the board with human-friendly positions for empty squares."""
    cells = [
        mark if mark != " " else "."
        for index, mark in enumerate(game.board)
    ]
    return "\n---+---+---\n".join(
        " | ".join(cells[row : row + 3]) for row in (0, 3, 6)
    )


def main() -> None:
    """Run an interactive two-player game."""
    game = Game()
    print("Boter, kaas en eieren")
    print("Choose a square by entering a number from 1 to 9.\n")

    model = MiniMax(game)

    while not game.winner() and not game.is_draw():
        print(render(game))
        if game.current_player == "X":
            move = model.best_move()
            print(f"AI (X) chooses square {move + 1}")
            game.move(move)
        else:
            choice = input(f"Player {game.current_player}, your move: ").strip()
            if choice == "q":
                print("Quitting the game.")
                return
            try:
                game.move(int(choice) - 1)
            except ValueError as error:
                print(f"Invalid move: {error}\n")

    print(render(game))
    print(f"Player {game.winner()} wins!" if game.winner() else "It's a draw!")


if __name__ == "__main__":
    main()
