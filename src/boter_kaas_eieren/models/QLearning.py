import random

from boter_kaas_eieren.game import Game


class QLearning:
    """A tabular Q-learning player for tic-tac-toe."""

    def __init__(
        self,
        game: Game,
        episodes: int = 10_000,
        learning_rate: float = 0.1,
        discount_factor: float = 0.9,
        exploration_rate: float = 0.2,
        seed: int | None = None,
    ) -> None:
        self.game = game
        self.episodes = episodes
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.q_table: dict[tuple[tuple[str, ...], str], dict[int, float]] = {}
        self._random = random.Random(seed)
        self._trained = False

    def best_move(self) -> int | None:
        """Return the best legal move for the game's current player."""
        if self.game.winner() or self.game.is_draw():
            return None

        if not self._trained:
            self.train()

        state = (tuple(self.game.board), self.game.current_player)
        legal_moves = self._legal_moves(self.game.board)
        values = self.q_table.get(state, {})
        return max(legal_moves, key=lambda move: values.get(move, 0.0))

    def train(self) -> None:
        """Learn action values by playing self-play training episodes."""
        for _ in range(self.episodes):
            board = [" "] * 9
            player = "X"

            while True:
                state = (tuple(board), player)
                legal_moves = self._legal_moves(board)
                action = self._training_move(state, legal_moves)
                board[action] = player

                winner = self._winner(board)
                next_player = self._other_player(player)
                if winner or not self._legal_moves(board):
                    reward = 1.0 if winner == player else 0.0
                    self._update(state, action, reward, None)
                    break

                next_state = (tuple(board), next_player)
                self._update(state, action, 0.0, next_state)
                player = next_player

        self._trained = True

    def _training_move(
        self,
        state: tuple[tuple[str, ...], str],
        legal_moves: list[int],
    ) -> int:
        if self._random.random() < self.exploration_rate:
            return self._random.choice(legal_moves)

        values = self.q_table.get(state, {})
        return max(legal_moves, key=lambda move: values.get(move, 0.0))

    def _update(
        self,
        state: tuple[tuple[str, ...], str],
        action: int,
        reward: float,
        next_state: tuple[tuple[str, ...], str] | None,
    ) -> None:

        # Q(s,a) ← Q(s,a) + α[target − Q(s,a)]
        
        values = self.q_table.setdefault(state, {})
        current_value = values.get(action, 0.0)
        if next_state is None:
            target = reward
        else:
            next_board, _ = next_state
            next_legal = self._legal_moves(next_board)
            next_values = self.q_table.get(next_state, {})
            best_next = max((next_values.get(a, 0.0) for a in next_legal), default=0.0)
            target = -self.discount_factor * best_next
        values[action] = current_value + self.learning_rate * (
            target - current_value
        )

    @staticmethod
    def _legal_moves(board: list[str] | tuple[str, ...]) -> list[int]:
        return [index for index, square in enumerate(board) if square == " "]

    @staticmethod
    def _other_player(player: str) -> str:
        return "O" if player == "X" else "X"

    @staticmethod
    def _winner(board: list[str]) -> str | None:
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
                board[first] != " "
                and board[first] == board[second] == board[third]
            ):
                return board[first]
        return None
