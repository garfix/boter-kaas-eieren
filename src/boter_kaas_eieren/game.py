"""Core rules for a two-player boter-kaas-en-eieren game."""

from dataclasses import dataclass, field
import random


class Game:
    """A 3x3 game where players alternate between X and O."""

    board: list[str]
    current_player: str

    def __init__(self, first_player: str = "X") -> None:
        """Initialize a new game."""
        self.board = [" "] * 9
        self.current_player = first_player

    def move(self, position: int) -> None:
        """Place the current player's mark at a zero-based position."""
        if not 0 <= position < 9:
            raise ValueError("position must be between 0 and 8")
        if self.board[position] != " ":
            raise ValueError("that square is already taken")
        if self.winner() or self.is_draw():
            raise ValueError("the game is already over")

        self.board[position] = self.current_player
        self.current_player = "O" if self.current_player == "X" else "X"

    def winner(self) -> str | None:
        """Return the winning mark, or None while there is no winner."""
        for first, second, third in (
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6),
        ):
            if (
                self.board[first] != " "
                and self.board[first] == self.board[second] == self.board[third]
            ):
                return self.board[first]
        return None

    def is_draw(self) -> bool:
        """Return whether every square is filled without a winner."""
        return self.winner() is None and all(square != " " for square in self.board)
