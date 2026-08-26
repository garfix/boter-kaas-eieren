"""Monte Carlo Tree Search for a boter-kaas-en-eieren game."""

from __future__ import annotations

import math
import random

from boter_kaas_eieren.game import Game

WINNING_LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


def _winner(board: list[str]) -> str | None:
    """Return the marks on ``board`` that fill a line, or None when there is none."""
    for first, second, third in WINNING_LINES:
        if board[first] != " " and board[first] == board[second] == board[third]:
            return board[first]
    return None


def _other(player: str) -> str:
    """Return the opponent of ``player``."""
    return "O" if player == "X" else "X"


class Node:
    """One board position inside the search tree."""

    def __init__(
        self,
        board: list[str],
        player: str,
        move: int | None = None,
        parent: Node | None = None,
    ) -> None:
        self.board = board
        self.player = player  # the player who is to move at this position
        self.move = move  # the move that led from the parent to this node
        self.parent = parent
        self.children: list[Node] = []
        self.visits = 0
        # wins recorded from the perspective of the player to move at this node
        self.wins = 0.0
        self.unplayed = [
            index for index, square in enumerate(board) if square == " "
        ]

    def is_done(self) -> bool:
        """Whether the game is over at this position (won or drawn)."""
        return _winner(self.board) is not None or not self.unplayed


class MonteCarloTreeSearch:
    """Find good moves by building a search tree only for the lines it explores.

    Unlike Minimax, MCTS never builds the complete game tree. It keeps a small
    tree of only the positions it visits, estimates every unvisited leaf by
    finishing the game with random moves (a "playout"), and stores how often
    each position was visited and won. This is what makes it scale to games
    like Go, where it is impossible to enumerate every reachable state.
    """

    def __init__(
        self,
        game: Game,
        iterations: int = 1000,
        exploration: float = math.sqrt(2),
        seed: int | None = None,
    ) -> None:
        self.game = game
        self.iterations = iterations
        self.exploration = exploration
        self._random = random.Random(seed)

    def best_move(self) -> int | None:
        """Return the best move for the game's current player."""
        if self.game.winner() or self.game.is_draw():
            return None

        root = Node(self.game.board[:], self.game.current_player)
        for _ in range(self.iterations):
            candidate = self._select(root)
            if not candidate.is_done():
                candidate = self._expand(candidate)
            outcome = self._simulate(candidate)
            self._backpropagate(candidate, outcome)

        best = max(root.children, key=lambda child: child.visits)
        return best.move

    def _select(self, node: Node) -> Node:
        """Drill down the tree, choosing the most promising child at each step."""
        while node.children and not node.unplayed:
            node = max(node.children, key=self._upper_confidence_bound)
        return node

    def _upper_confidence_bound(self, child: Node) -> float:
        """UCB1 = exploitation + exploration, negated for the parent's perspective."""
        if child.visits == 0:
            return math.inf
        # child.wins is from the opponent's perspective (the player to move at
        # the child), so flip its sign to score the move for the parent.
        exploitation = -child.wins / child.visits
        exploration = self.exploration * math.sqrt(
            math.log(child.parent.visits) / child.visits
        )
        return exploitation + exploration

    def _expand(self, node: Node) -> Node:
        """Give ``node`` one new child by playing a legal, still untried move."""
        move = self._random.choice(node.unplayed)
        node.unplayed.remove(move)

        board = node.board[:]
        board[move] = node.player
        child = Node(board, _other(node.player), move=move, parent=node)
        node.children.append(child)
        return child

    def _simulate(self, node: Node) -> float:
        """Finish the game at random and score it for ``node``'s player to move."""
        board = node.board[:]
        player = node.player
        winner = _winner(board)
        while winner is None and not self._is_full(board):
            moves = [i for i, square in enumerate(board) if square == " "]
            board[self._random.choice(moves)] = player
            winner = _winner(board)
            player = _other(player)

        if winner is None:
            return 0.0
        return 1.0 if winner == node.player else -1.0

    def _is_full(self, board: list[str]) -> bool:
        """Return whether every square on ``board`` is occupied."""
        return all(square != " " for square in board)

    def _backpropagate(self, node: Node, result: float) -> None:
        """Push ``result`` up the tree, flipping its sign (zero-sum) at each layer."""
        while node is not None:
            node.visits += 1
            node.wins += result
            result = -result
            node = node.parent
    