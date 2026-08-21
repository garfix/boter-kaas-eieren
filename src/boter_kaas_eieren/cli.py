"""Terminal interface for boter-kaas-en-eieren."""

from .game import Game


def render(game: Game) -> str:
    """Render the board with human-friendly positions for empty squares."""
    cells = [
        mark if mark != " " else str(index + 1)
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

    while not game.winner and not game.is_draw:
        print(render(game))
        choice = input(f"Player {game.current_player}, your move: ").strip()
        try:
            game.move(int(choice) - 1)
        except ValueError as error:
            print(f"Invalid move: {error}\n")

    print(render(game))
    print(f"Player {game.winner} wins!" if game.winner else "It's a draw!")


if __name__ == "__main__":
    main()
